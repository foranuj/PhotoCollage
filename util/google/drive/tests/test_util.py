import unittest

from util.google.drive.util import upload_to_folder, get_credentials, get_file_id_from_url, upload_with_item_check


class MyTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        print('BasicTest.__init__')
        super(MyTestCase, self).__init__(*args, **kwargs)

    def test_file_upload(self):
        pdf_file_path = "/Users/anshah/YearbookCreatorOut/anshah/pdf_outputs/Monticello_Preschool_2021_2022_Sunshine_Ryan Yu_cover.pdf"
        upload_to_folder('1JYbuVmoCUxf1wuvkk8izPhC7jgRdR2rd', pdf_file_path)

    def test_check_file_exists(self):
        from googleapiclient.discovery import build

        file_id = "1JYbuVmoCUxf1wuvkk8izPhC7jgRdR2rd"
        service = build('drive', 'v3', credentials=get_credentials())

        g_file = service.files().get(fileId=file_id, fields='parents').execute()
        print(g_file)
        assert g_file == {'parents': ['0AI0gvbmOqne8Uk9PVA']}

    def test_get_file_id_from_url(self):
        url = "https://www.googleapis.com/drive/v3/files/1y23-i7A8TmRG7X1y0le11WNcPGz8UfbD?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
        file_id = get_file_id_from_url(url)
        assert file_id == '1y23-i7A8TmRG7X1y0le11WNcPGz8UfbD'
        #https://drive.google.com/file/d/1y23-i7A8TmRG7X1y0le11WNcPGz8UfbD/view?usp=sharing

    def test_upload_with_file_check(self):
        interior_pdf = "/Users/ashah/YearbookCreatorOut/ashah/pdf_outputs/Monticello_Preschool_2021_2022_Sunshine_Ryan Yu_back_cover.pdf"
        interior_url = 'https://www.googleapis.com/drive/v3/files/1y23-i7A8TmRG7X1y0le11WNcPGz8UfbD?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc'
        file_id = get_file_id_from_url(interior_url)
        upload_with_item_check('1JYbuVmoCUxf1wuvkk8izPhC7jgRdR2rd',
                               interior_pdf,
                               file_id)
if __name__ == '__main__':
    unittest.main()
