import unittest

from util.dropbox.util import upload_file


class MyTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        print('BasicTest.__init__')
        super(MyTestCase, self).__init__(*args, **kwargs)

    def test_file_upload(self):
        pdf_file_path = "/Users/anshah/Desktop/chunk_40"
        upload_file(pdf_file_path, "testingChunk_first_try")
