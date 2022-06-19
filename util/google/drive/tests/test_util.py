import unittest

from util.google.drive.util import upload_to_folder, get_credentials


class MyTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        print('BasicTest.__init__')
        super(MyTestCase, self).__init__(*args, **kwargs)

    def test_file_upload(self):
        pdf_file_path = "/Users/anshah/YearbookCreatorOut/anshah/pdf_outputs/Monticello_Preschool_2021_2022_Sunshine_Ryan Yu_cover.pdf"
        upload_to_folder('1JYbuVmoCUxf1wuvkk8izPhC7jgRdR2rd', pdf_file_path)

    def test_check_file_exists(self):
        from googleapiclient.discovery import build

        file_id = "1ADcULAXEEEkWqHV_7Qkdt6oYsBi2q7pw"
        service = build('drive', 'v3', credentials=get_credentials())

        g_file = service.files().get(fileId=file_id, fields='parents').execute()
        print(g_file)

if __name__ == '__main__':
    unittest.main()
