import unittest
from typing import Optional, List

from data.sqllite.reader import get_album_details_for_school, get_child_orders, get_desired_name, create_connection, \
    get_order_details_for_child
import getpass
import os

school_name = "VargasElementary"


def print_row(store, treepath, treeiter):
    print("\t" * (treepath.get_depth() - 1), store[treeiter][:], sep="")


class TestReader(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        print('BasicTest.__init__')
        super(TestReader, self).__init__(*args, **kwargs)
        self.output_base_dir = os.path.join('/Users', getpass.getuser(), 'YearbookCreatorOut')
        self.input_base_dir = os.path.join('/Users', getpass.getuser(), 'GoogleDrive', 'YearbookCreatorInput')
        self.yearbook_parameters = {'max_count': 12,
                                    'db_file_path': os.path.join(self.input_base_dir, 'RY_Monticello.db'),
                                    'output_dir': os.path.join(self.output_base_dir, getpass.getuser()),
                                    'corpus_base_dir': os.path.join('/Users', getpass.getuser(), 'GoogleDrive',
                                                                    school_name)}

    def test_get_order_details_for_child(self):
        orders = get_order_details_for_child(create_connection(self.yearbook_parameters['db_file_path']), "Aarish Mathur")

        print("Printing orders for Shannon")
        [print(order) for order in orders]
        print("Done Printing orders for Shannon")

    def test_get_album_details(self):
        album_details = get_album_details_for_school(self.yearbook_parameters['db_file_path'],
                                                     'Monticello_Preschool_2021_2022')
        for row in album_details:
            print(row)

    def test_get_order_details_for_child(self):
        # Srivardhan Srinivasan
        order_details: Optional[List[(str, str)]] = get_child_orders(self.yearbook_parameters['db_file_path'],
                                                                     child_name='Aarish Mathur')

        print(order_details)

        assert (len(order_details) == 1)
        assert (order_details[0] == 'Digital', '10039')

    def test_desired_name(self):
        order_id = '10067'

        desired_name = get_desired_name(create_connection(self.yearbook_parameters['db_file_path']), order_id)
        assert (desired_name == 'Elvis Ocegueda')


if __name__ == '__main__':
    unittest.main()
