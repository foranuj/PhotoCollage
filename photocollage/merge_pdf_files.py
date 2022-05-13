import argparse
import subprocess
import os.path
import sys
import shutil
import getpass
import gi
from gi.repository.Gtk import TreeStore
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, Gdk, GObject, GdkPixbuf  # noqa: E402, I100


from data.model.ModelCreator import get_tree_model

corpus_base_dir = os.path.join('/Users', getpass.getuser(), 'GoogleDrive')
output_base_dir = os.path.join('/Users', getpass.getuser(), 'YearbookCreatorOut')
input_base_dir = os.path.join(corpus_base_dir, 'YearbookCreatorInput')

yearbook_parameters = {'max_count': 12,
                       'db_file_path': os.path.join(input_base_dir, 'RY_Small_New.db'),
                       'output_dir': os.path.join(output_base_dir, getpass.getuser()),
                       'corpus_base_dir': corpus_base_dir}


def merge_pdfs(store: Gtk.TreeStore, treepath: Gtk.TreePath, treeiter: Gtk.TreeIter):


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-indir', help='Path of the pdfs directory')
    parser.add_argument('-outdir', help='Path of the output pdfs directory ')
    parser.add_argument('-pickledir', help='Path of pickle files to read')
    parser.add_argument('-c', '--compress', type=int, help='Compression level from 0 to 4')

    args = parser.parse_args()

    tree_model = get_tree_model(yearbook_parameters, "VargasElementary")

    tree_model.foreach(merge_pdfs)
