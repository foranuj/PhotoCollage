# Copyright (C) 2013 Adrien Vergé
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import copy
import gettext
from io import BytesIO
import math
import os.path
import random
import sys
import urllib

import cairo
import gi

from photocollage import APP_NAME, artwork, collage, render
from photocollage.render import PIL_SUPPORTED_EXTS as EXTS
from photocollage.dialogs.ConfigSelectorDialog import ConfigSelectorDialog
from photocollage.dialogs.SettingsDialog import SettingsDialog

from data.readers.default import corpus_processor
from yearbook.Yearbook import create_yearbook_metadata

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, GdkPixbuf  # noqa: E402, I100


gettext.textdomain(APP_NAME)
_ = gettext.gettext
_n = gettext.ngettext


# xgettext --keyword=_n:1,2 -o po/photocollage.pot $(find . -name '*.py')
# cp po/photocollage.pot po/fr.po
# msgfmt -o po/fr.mo po/fr.po


def pil_image_to_cairo_surface(src):
    # TODO: cairo.ImageSurface.create_for_data() is not yet available in
    # Python 3, so we use PNG as an intermediate.
    buf = BytesIO()
    src.save(buf, "png")
    buf.seek(0)
    surface = cairo.ImageSurface.create_from_png(buf)
    buf.close()
    return surface


def get_all_save_image_exts():
    all_types = dict(list(EXTS.RW.items()) + list(EXTS.WO.items()))
    all_images = []
    for file_type in all_types:
        for ext in all_types[file_type]:
            all_images.append(ext)

    return all_images


def set_open_image_filters(dialog):
    """Set our own filter because Gtk.FileFilter.add_pixbuf_formats() contains
    formats not supported by PIL.

    """
    # Do not show the filter to the user, just limit selectable files
    img_filter = Gtk.FileFilter()
    img_filter.set_name(_("All supported image formats"))

    all_types = dict(list(EXTS.RW.items()) + list(EXTS.RO.items()))
    for type in all_types:
        for ext in all_types[type]:
            img_filter.add_pattern("*." + ext)
            img_filter.add_pattern("*." + ext.upper())

    dialog.add_filter(img_filter)
    dialog.set_filter(img_filter)


def set_save_image_filters(dialog):
    """Set our own filter because Gtk.FileFilter.add_pixbuf_formats() contains
    formats not supported by PIL.

    """
    all_types = dict(list(EXTS.RW.items()) + list(EXTS.WO.items()))
    filters = [Gtk.FileFilter()]

    flt = filters[-1]
    flt.set_name(_("All supported image formats"))
    for ext in get_all_save_image_exts():
        flt.add_pattern("*." + ext)
        flt.add_pattern("*." + ext.upper())
    dialog.add_filter(flt)
    dialog.set_filter(flt)

    for file_type in all_types:
        filters.append(Gtk.FileFilter())
        flt = filters[-1]
        name = _("%s image") % file_type
        name += " (." + ", .".join(all_types[file_type]) + ")"
        flt.set_name(name)
        for ext in all_types[file_type]:
            flt.add_pattern("*." + ext)
            flt.add_pattern("*." + ext.upper())
        dialog.add_filter(flt)


def gtk_run_in_main_thread(fn):
    def my_fn(*args, **kwargs):
        GObject.idle_add(fn, *args, **kwargs)

    return my_fn


class UserCollage:
    """Represents a user-defined collage

    A UserCollage contains a list of photos (referenced by filenames) and a
    collage.Page object describing their layout in a final poster.

    """

    def __init__(self, photolist):
        self.photolist = photolist

    def make_page(self, opts):
        # Define the output image height / width ratio
        ratio = 1.0 * opts.out_h / opts.out_w

        # Compute a good number of columns. It depends on the ratio, the number
        # of images and the average ratio of these images. According to my
        # calculations, the number of column should be inversely proportional
        # to the square root of the output image ratio, and proportional to the
        # square root of the average input images ratio.
        avg_ratio = (sum(1.0 * photo.h / photo.w for photo in self.photolist) /
                     len(self.photolist))
        # Virtual number of images: since ~ 1 image over 3 is in a multi-cell
        # (i.e. takes two columns), it takes the space of 4 images.
        # So it's equivalent to 1/3 * 4 + 2/3 = 2 times the number of images.
        virtual_no_imgs = 2 * len(self.photolist)
        no_cols = int(round(math.sqrt(avg_ratio / ratio * virtual_no_imgs)))

        self.page = collage.Page(1.0, ratio, no_cols)
        random.shuffle(self.photolist)
        for photo in self.photolist:
            self.page.add_cell(photo)
        self.page.adjust()

    def duplicate(self):
        return UserCollage(copy.copy(self.photolist))


class MainWindow(Gtk.Window):
    TARGET_TYPE_TEXT = 1
    TARGET_TYPE_URI = 2

    def __init__(self):
        super().__init__(title=_("Yearbook Creator"))
        self.yearbook_configurator = Gtk.Button(label=_("Yearbook Settings..."))
        self.btn_choose_images = Gtk.Button(label=_("Add images..."))
        self.img_preview = ImagePreviewArea(self)
        self.btn_settings = Gtk.Button()
        self.btn_new_layout = Gtk.Button(label=_("Regenerate"))
        self.btn_redo = Gtk.Button()
        self.lbl_history_index = Gtk.Label(" ")
        self.btn_undo = Gtk.Button()
        self.btn_save = Gtk.Button(label=_("Save poster..."))
        self.history = []
        self.history_index = 0

        class Options:
            def __init__(self):
                self.border_w = 0.01
                self.border_c = "blue"
                self.out_w = 2550
                self.out_h = 3300

        self.opts = Options()

        self.make_window()

    def make_window(self):
        self.set_border_width(10)

        box_window = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        self.add(box_window)

        # -----------------------
        #  Input and output pan
        # -----------------------

        box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.HORIZONTAL)
        box_window.pack_start(box, False, False, 0)

        self.yearbook_configurator.connect("clicked", self.setup_yearbook_config)
        box.pack_start(self.yearbook_configurator, False, False, 0)

        self.btn_choose_images.set_image(Gtk.Image.new_from_stock(
            Gtk.STOCK_OPEN, Gtk.IconSize.LARGE_TOOLBAR))
        self.btn_choose_images.set_always_show_image(True)
        self.btn_choose_images.connect("clicked", self.choose_images)
        box.pack_start(self.btn_choose_images, False, False, 0)

        self.btn_save.set_image(Gtk.Image.new_from_stock(
            Gtk.STOCK_SAVE_AS, Gtk.IconSize.LARGE_TOOLBAR))
        self.btn_save.set_always_show_image(True)
        self.btn_save.connect("clicked", self.save_poster)
        box.pack_start(self.btn_save, False, False, 0)

        # -----------------------
        #  Tools pan
        # -----------------------

        box.pack_start(Gtk.SeparatorToolItem(), True, True, 0)

        self.btn_undo.set_image(Gtk.Image.new_from_stock(
            Gtk.STOCK_UNDO, Gtk.IconSize.LARGE_TOOLBAR))
        self.btn_undo.connect("clicked", self.select_prev_layout)
        box.pack_start(self.btn_undo, False, False, 0)
        box.pack_start(self.lbl_history_index, False, False, 0)
        self.btn_redo.set_image(Gtk.Image.new_from_stock(
            Gtk.STOCK_REDO, Gtk.IconSize.LARGE_TOOLBAR))
        self.btn_redo.connect("clicked", self.select_next_layout)
        box.pack_start(self.btn_redo, False, False, 0)
        self.btn_new_layout.set_image(Gtk.Image.new_from_stock(
            Gtk.STOCK_REFRESH, Gtk.IconSize.LARGE_TOOLBAR))
        self.btn_new_layout.set_always_show_image(True)
        self.btn_new_layout.connect("clicked", self.regenerate_layout)
        box.pack_start(self.btn_new_layout, False, False, 0)

        box.pack_start(Gtk.SeparatorToolItem(), True, True, 0)

        self.btn_settings.set_image(Gtk.Image.new_from_stock(
            Gtk.STOCK_PREFERENCES, Gtk.IconSize.LARGE_TOOLBAR))
        self.btn_settings.set_always_show_image(True)
        self.btn_settings.connect("clicked", self.set_settings)
        box.pack_end(self.btn_settings, False, False, 0)

        # -------------------
        #  Children Tree View
        # -------------------
        box = Gtk.Box(spacing=10)
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.add(self.child_list_view)
        box.pack_start(self.scrollable_treelist, True, True, 0)

        # -------------------
        #  Image preview pan
        # -------------------

        box = Gtk.Box(spacing=10)
        box_window.pack_start(box, True, True, 0)

        self.img_preview.set_size_request(600, 400)
        self.img_preview.connect("drag-data-received", self.on_drag)
        self.img_preview.drag_dest_set(Gtk.DestDefaults.ALL, [],
                                       Gdk.DragAction.COPY)
        targets = Gtk.TargetList.new([])
        targets.add_text_targets(MainWindow.TARGET_TYPE_TEXT)
        targets.add_uri_targets(MainWindow.TARGET_TYPE_URI)
        self.img_preview.drag_dest_set_target_list(targets)

        box.pack_start(self.img_preview, True, True, 0)

        self.btn_save.set_sensitive(False)

        self.btn_undo.set_sensitive(False)
        self.btn_redo.set_sensitive(False)

        self.update_photolist([])

    def update_photolist(self, new_images):
        try:
            photolist = []
            if self.history_index < len(self.history):
                photolist = copy.copy(
                    self.history[self.history_index].photolist)
            photolist.extend(render.build_photolist(new_images))

            if len(photolist) > 0:
                new_collage = UserCollage(photolist)
                new_collage.make_page(self.opts)
                self.render_from_new_collage(new_collage)
            else:
                self.update_tool_buttons()
        except render.BadPhoto as e:
            dialog = ErrorDialog(
                self, _("This image could not be opened:\n\"%(imgname)s\".")
                      % {"imgname": e.photoname})
            dialog.run()
            dialog.destroy()

    def setup_yearbook_config(self, button):
        dialog = ConfigSelectorDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print(dialog.config_parameters)
            corpus = corpus_processor(dialog.config_parameters["processed_corpus_file"])

            events = corpus.get_events()
            children = corpus.get_children()

            # Read the config file
            yearbook = create_yearbook_metadata(dialog.config_parameters["config_file"], "","")
            corpus_dir = dialog.config_parameters["corpus_dir"]
            # Fix a child
            child = "Rilee"
            for page in yearbook.pages:
                if not page.personalized:
                    print("Skipping this page, %s" % page.event_name)
                    continue

                print("Working on page: (%s, %s, %s)" % (page.image, page.event_name, page.number))
                _images_per_event = corpus.events_to_images[page.event_name]

                child_images_per_event = corpus.get_child_images_for_event_with_scores(child, page.event_name)
                print("Images per event: (%s) " % str(len(child_images_per_event)))

                filenames = [os.path.join(corpus_dir, page.event_name, a_tuple[0]) for a_tuple in child_images_per_event]
                self.update_photolist(filenames)
                break

            dialog.destroy()
            if self.history:
                self.render_preview()
        else:
            dialog.destroy()

    def choose_images(self, button):
        dialog = PreviewFileChooserDialog(title=_("Choose images"),
                                          parent=button.get_toplevel(),
                                          action=Gtk.FileChooserAction.OPEN,
                                          select_multiple=True,
                                          modal=True)

        if dialog.run() == Gtk.ResponseType.OK:
            files = dialog.get_filenames()
            dialog.destroy()
            self.update_photolist(files)
        else:
            dialog.destroy()

    def on_drag(self, widget, drag_context, x, y, data, info, time):
        if info == MainWindow.TARGET_TYPE_TEXT:
            files = data.get_text().splitlines()
        elif info == MainWindow.TARGET_TYPE_URI:
            # Can only handle local URIs
            files = [f for f in data.get_uris() if f.startswith("file://")]

        for i in range(len(files)):
            if files[i].startswith("file://"):
                files[i] = urllib.parse.unquote(files[i][7:])
        self.update_photolist(files)

    def render_preview(self):
        collage = self.history[self.history_index]

        # If the desired ratio changed in the meantime (e.g. from landscape to
        # portrait), it needs to be re-updated
        collage.page.target_ratio = 1.0 * self.opts.out_h / self.opts.out_w
        collage.page.adjust_cols_heights()

        w = self.img_preview.get_allocation().width
        h = self.img_preview.get_allocation().height
        collage.page.scale_to_fit(w, h)

        # Display a "please wait" dialog and do the job.
        compdialog = ComputingDialog(self)

        def on_update(img, fraction_complete):
            self.img_preview.set_collage(img, collage)
            compdialog.update(fraction_complete)

        def on_complete(img):
            self.img_preview.set_collage(img, collage)
            compdialog.destroy()
            self.btn_save.set_sensitive(True)

        def on_fail(exception):
            dialog = ErrorDialog(self, "{}:\n\n{}".format(
                _("An error occurred while rendering image:"), exception))
            compdialog.destroy()
            dialog.run()
            dialog.destroy()
            self.btn_save.set_sensitive(False)

        t = render.RenderingTask(
            collage.page,
            border_width=self.opts.border_w * max(collage.page.w,
                                                  collage.page.h),
            border_color=self.opts.border_c,
            on_update=gtk_run_in_main_thread(on_update),
            on_complete=gtk_run_in_main_thread(on_complete),
            on_fail=gtk_run_in_main_thread(on_fail))
        t.start()

        response = compdialog.run()
        if response == Gtk.ResponseType.CANCEL:
            t.abort()
            compdialog.destroy()

    def render_from_new_collage(self, collage):
        self.history.append(collage)
        self.history_index = len(self.history) - 1
        self.update_tool_buttons()
        self.render_preview()

    def regenerate_layout(self, button=None):
        new_collage = self.history[self.history_index].duplicate()
        new_collage.make_page(self.opts)
        self.render_from_new_collage(new_collage)

    def select_prev_layout(self, button):
        self.history_index -= 1
        self.update_tool_buttons()
        self.render_preview()

    def select_next_layout(self, button):
        self.history_index += 1
        self.update_tool_buttons()
        self.render_preview()

    def set_settings(self, button):
        dialog = SettingsDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.apply_opts(self.opts)
            dialog.destroy()
            if self.history:
                self.render_preview()
        else:
            dialog.destroy()

    def save_poster(self, button):
        collage = self.history[self.history_index]

        enlargement = float(self.opts.out_w) / collage.page.w
        collage.page.scale(enlargement)

        dialog = Gtk.FileChooserDialog(_("Save image"), button.get_toplevel(),
                                       Gtk.FileChooserAction.SAVE)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        dialog.set_do_overwrite_confirmation(True)
        set_save_image_filters(dialog)
        if dialog.run() != Gtk.ResponseType.OK:
            dialog.destroy()
            return
        savefile = dialog.get_filename()
        base, ext = os.path.splitext(savefile)
        if ext == "" or not ext[1:].lower() in get_all_save_image_exts():
            savefile += ".jpg"
        dialog.destroy()

        # Display a "please wait" dialog and do the job.
        compdialog = ComputingDialog(self)

        def on_update(img, fraction_complete):
            compdialog.update(fraction_complete)

        def on_complete(img):
            compdialog.destroy()

        def on_fail(exception):
            dialog = ErrorDialog(self, "{}:\n\n{}".format(
                _("An error occurred while rendering image:"), exception))
            compdialog.destroy()
            dialog.run()
            dialog.destroy()

        t = render.RenderingTask(
            collage.page, output_file=savefile,
            border_width=self.opts.border_w * max(collage.page.w,
                                                  collage.page.h),
            border_color=self.opts.border_c,
            on_update=gtk_run_in_main_thread(on_update),
            on_complete=gtk_run_in_main_thread(on_complete),
            on_fail=gtk_run_in_main_thread(on_fail))
        t.start()

        response = compdialog.run()
        if response == Gtk.ResponseType.CANCEL:
            t.abort()
            compdialog.destroy()

    def update_tool_buttons(self):
        self.btn_undo.set_sensitive(self.history_index > 0)
        self.btn_redo.set_sensitive(self.history_index < len(self.history) - 1)
        if self.history_index < len(self.history):
            self.lbl_history_index.set_label(str(self.history_index + 1))
        else:
            self.lbl_history_index.set_label(" ")
        self.btn_save.set_sensitive(
            self.history_index < len(self.history))
        self.btn_new_layout.set_sensitive(
            self.history_index < len(self.history))


class ImagePreviewArea(Gtk.DrawingArea):
    """Area to display the poster preview and react to user actions"""
    INSENSITIVE, FLYING, SWAPPING_OR_MOVING = range(3)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        parse, color = Gdk.Color.parse("#888888")
        self.modify_bg(Gtk.StateType.NORMAL, color)

        # http://www.pygtk.org/pygtk2tutorial/sec-EventHandling.html
        # https://developer.gnome.org/gdk3/stable/gdk3-Events.html#GdkEventMask
        self.connect("draw", self.draw)
        self.connect("motion-notify-event", self.motion_notify_event)
        self.connect("leave-notify-event", self.motion_notify_event)
        self.connect("button-press-event", self.button_press_event)
        self.connect("button-release-event", self.button_release_event)
        self.set_events(Gdk.EventMask.EXPOSURE_MASK |
                        Gdk.EventMask.LEAVE_NOTIFY_MASK |
                        Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK |
                        Gdk.EventMask.POINTER_MOTION_MASK)

        self.image = None
        self.mode = self.INSENSITIVE

        class SwapEnd:
            def __init__(self, cell=None, x=0, y=0):
                self.cell = cell
                self.x = x
                self.y = y

        self.x, self.y = 0, 0
        self.swap_origin = SwapEnd()
        self.swap_dest = SwapEnd()

    def set_collage(self, image, collage):
        self.image = pil_image_to_cairo_surface(image)
        # The Collage object must be deeply copied.
        # Otherwise, SWAPPING_OR_MOVING photos in a new page would also affect
        # the original page (in history).
        # The deep copy is done here (not in button_release_event) because
        # references to cells are gathered in other functions, so that making
        # the copy at the end would invalidate these references.
        self.collage = copy.deepcopy(collage)
        self.mode = self.FLYING
        self.queue_draw()

    def get_image_offset(self):
        return (round((self.get_allocation().width -
                       self.image.get_width()) / 2.0),
                round((self.get_allocation().height -
                       self.image.get_height()) / 2.0))

    def get_pos_in_image(self, x, y):
        if self.image is not None:
            x0, y0 = self.get_image_offset()
            return int(round(x - x0)), int(round(y - y0))
        return int(round(x)), int(round(y))

    def paint_image_border(self, context, cell, dash=None):
        x0, y0 = self.get_image_offset()

        context.set_source_rgb(1.0, 1.0, 0.0)
        context.set_line_width(2)
        if dash is not None:
            context.set_dash(dash)
        context.rectangle(x0 + cell.x + 1, y0 + cell.y + 1,
                          cell.w - 2, cell.h - 2)
        context.stroke()

    def paint_image_delete_button(self, context, cell):
        x0, y0 = self.get_image_offset()

        x = x0 + cell.x + cell.w - 12
        y = y0 + cell.y + 12

        context.arc(x, y, 8, 0, 6.2832)
        context.set_source_rgb(0.8, 0.0, 0.0)
        context.fill()
        context.arc(x, y, 8, 0, 6.2832)
        context.set_source_rgb(0.0, 0.0, 0.0)
        context.set_line_width(1)
        context.move_to(x - 4, y - 4)
        context.line_to(x + 4, y + 4)
        context.move_to(x - 4, y + 4)
        context.line_to(x + 4, y - 4)
        context.stroke()

    def draw(self, widget, context):
        if self.image is not None:
            x0, y0 = self.get_image_offset()
            context.set_source_surface(self.image, x0, y0)
            context.paint()

            if self.mode == self.FLYING:
                cell = self.collage.page.get_cell_at_position(self.x, self.y)
                if cell:
                    self.paint_image_border(context, cell)
                    self.paint_image_delete_button(context, cell)
            elif self.mode == self.SWAPPING_OR_MOVING:
                self.paint_image_border(context, self.swap_origin.cell, (3, 3))
                cell = self.collage.page.get_cell_at_position(self.x, self.y)
                if cell and cell != self.swap_origin.cell:
                    self.paint_image_border(context, cell, (3, 3))
        else:
            # Display the drag & drop image
            dnd_image = artwork.load_cairo_surface(artwork.ICON_DRAG_AND_DROP)
            context.set_source_surface(
                dnd_image,
                round((self.get_allocation().width -
                       dnd_image.get_width()) / 2.0),
                round((self.get_allocation().height -
                       dnd_image.get_height()) / 2.0))
            context.paint()

        return False

    def motion_notify_event(self, widget, event):
        self.x, self.y = self.get_pos_in_image(event.x, event.y)
        widget.queue_draw()

    def button_press_event(self, widget, event):
        if self.mode == self.FLYING:
            x, y = self.get_pos_in_image(event.x, event.y)
            cell = self.collage.page.get_cell_at_position(x, y)
            if not cell:
                return
            # Has the user clicked the delete button?
            dist = (cell.x + cell.w - 12 - x) ** 2 + (cell.y + 12 - y) ** 2
            if dist <= 8 * 8:
                self.collage.photolist.remove(cell.photo)
                if self.collage.photolist:
                    self.collage.make_page(self.parent.opts)
                    self.parent.render_from_new_collage(self.collage)
                else:
                    self.image = None
                    self.mode = self.INSENSITIVE
                    self.parent.history_index = len(self.parent.history)
                    self.parent.update_tool_buttons()
            # Otherwise, the user wants to swap this image with another
            else:
                self.swap_origin.x, self.swap_origin.y = x, y
                self.swap_origin.cell = cell
                self.mode = self.SWAPPING_OR_MOVING
        widget.queue_draw()

    def button_release_event(self, widget, event):
        if self.mode == self.SWAPPING_OR_MOVING:
            self.swap_dest.x, self.swap_dest.y = \
                self.get_pos_in_image(event.x, event.y)
            self.swap_dest.cell = self.collage.page.get_cell_at_position(
                self.swap_dest.x, self.swap_dest.y)
            if self.swap_dest.cell \
                    and self.swap_origin.cell != self.swap_dest.cell:
                # different cell: SWAPPING
                self.collage.page.swap_photos(self.swap_origin.cell,
                                              self.swap_dest.cell)
                self.parent.render_from_new_collage(self.collage)
            elif self.swap_dest.cell:
                # same cell: MOVING
                move_x = (self.swap_origin.x - self.x) / self.swap_dest.cell.w
                move_y = (self.swap_origin.y - self.y) / self.swap_dest.cell.h
                self.swap_dest.cell.photo.move(move_x, move_y)
                self.parent.render_from_new_collage(self.collage)
            self.mode = self.FLYING
        widget.queue_draw()


class ComputingDialog(Gtk.Dialog):
    """Simple "please wait" dialog, with a "cancel" button"""

    def __init__(self, parent):
        super().__init__(
            _("Please wait"), parent, 0, (Gtk.STOCK_CANCEL,
                                          Gtk.ResponseType.CANCEL))
        self.set_default_size(300, -1)
        self.set_border_width(10)

        box = self.get_content_area()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.add(vbox)

        label = Gtk.Label(_("Performing image computation..."))
        vbox.pack_start(label, True, True, 0)

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_fraction(0)
        vbox.pack_start(self.progressbar, True, True, 0)

        self.show_all()

    def update(self, fraction):
        self.progressbar.set_fraction(fraction)


class ErrorDialog(Gtk.Dialog):
    def __init__(self, parent, message):
        super().__init__(_("Error"), parent, 0,
                         (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_border_width(10)
        box = self.get_content_area()
        box.add(Gtk.Label(message))
        self.show_all()


class PreviewFileChooserDialog(Gtk.FileChooserDialog):
    PREVIEW_MAX_SIZE = 256

    def __init__(self, **kw):
        super().__init__(**kw)

        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        set_open_image_filters(self)

        self._preview = Gtk.Image()
        # Don't let preview size down horizontally for skinny images, cause
        # that looks distracting
        self._preview.set_size_request(
            PreviewFileChooserDialog.PREVIEW_MAX_SIZE, -1)
        self.set_preview_widget(self._preview)
        self.set_use_preview_label(False)
        self.connect("update-preview", self.update_preview_cb)

    def update_preview_cb(self, file_chooser):
        filename = self.get_preview_filename()
        if filename is None or os.path.isdir(filename):
            self.set_preview_widget_active(False)
            return
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                filename,
                PreviewFileChooserDialog.PREVIEW_MAX_SIZE,
                PreviewFileChooserDialog.PREVIEW_MAX_SIZE)
            self._preview.set_from_pixbuf(pixbuf)
        except Exception as e:
            print(e)
            self.set_preview_widget_active(False)
            return
        self.set_preview_widget_active(True)


def main():
    # Enable threading. Without that, threads hang!
    GObject.threads_init()

    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()

    # If arguments are given, treat them as input images
    if len(sys.argv) > 1:
        win.update_photolist(sys.argv[1:])

    Gtk.main()
