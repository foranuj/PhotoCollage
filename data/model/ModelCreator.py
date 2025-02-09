from functools import reduce

import gi

from data.sqllite.reader import create_connection, get_schools, get_all_rows, get_order_details_for_child

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from yearbook.Yearbook import Yearbook, create_yearbook


def get_school_list_model(db_file: str):
    from gi.repository import Gtk

    school_list_store = Gtk.ListStore(str)
    # Create a connection to the database
    conn = create_connection(db_file)

    all_schools = get_schools(conn)
    for school in all_schools:
        school_list_store.append(school)

    conn.close()
    return school_list_store


# This is the main entry method that takes the sqlite data base file and returns the final tree model
def get_tree_model(dir_params: {}, school_selection: str) -> Gtk.TreeStore:
    print("*********Retrieving the entire tree model********")

    treestore = Gtk.TreeStore(Yearbook)

    db_file = dir_params['db_file_path']
    # Create a connection to the database
    conn = create_connection(db_file)

    all_rows = get_all_rows(conn)
    added_schools = {}

    count_children = 0
    for row in all_rows:
        school_name = ('%s' % row[0]).strip()
        if school_selection != school_name:
            continue

        if school_name not in added_schools.keys():
            # add this school as a parent to the tree
            # Create the school level yearbook here
            school_yearbook = create_yearbook(dir_params, school_name, classroom=None, child=None)
            school_parent = treestore.append(None, [school_yearbook])
            added_schools[school_name] = {}

        current_class = ('%s' % row[1]).strip()
        if current_class not in added_schools[school_name].keys():
            class_yearbook = create_yearbook(dir_params, school_name, classroom=current_class,
                                             child=None, parent_book=school_yearbook.pickle_yearbook)
            class_parent = treestore.append(school_parent, [class_yearbook])
            added_schools[school_name][current_class] = {}

        current_child = ('%s' % row[2]).strip()
        if current_child not in added_schools[school_name][current_class].keys():
            child_yearbook = create_yearbook(dir_params, school_name, classroom=current_class,
                                             child=current_child,
                                             parent_book=class_yearbook.pickle_yearbook)

            if child_yearbook is not None:
                # has_optional_pages = reduce(lambda x, y: x or y, [page.is_optional for page in child_yearbook.pages])
                # if has_optional_pages:
                if len(child_yearbook.orders) > 0:
                    print("CHILD HAS AN ORDER PLACED, SO ADDING TO TREE")
                    treestore.append(class_parent, [child_yearbook])
                    added_schools[school_name][current_class][current_child] = {}
                    count_children = count_children + 1

    print("Total number of children added %s" % count_children)
    conn.close()
    return treestore
