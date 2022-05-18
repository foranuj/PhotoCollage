import dropbox


app_key = "fokjaosciy64j91"
app_secret = "bq91t4p0g2gyfqz"

DROPBOX_ROOT_PATH = "/vargas_yearbooks/"

dropbox_access_token = "sl.BHuzBs8bJyeKqzHbU3opMEdzxEulv_W_1yzikInQZq_In40nHkWJRWn1oty0FpjnvnMYotmSJOGwJTQYlylcxIn1T1B-CUw4c4WBBo5b3GLregVEoEn0mKHpF53QW9EpM8l5RW-jzdNe"
client = dropbox.Dropbox(dropbox_access_token)
print("[SUCCESS] dropbox account linked")


def get_download_url_from_file(path):
    try:
        link = client.sharing_create_shared_link_with_settings(path)
        print(link.url)
        return link.url[:-1] + "1"
    except Exception as exception:
        error_string = str(exception)
        print(error_string.split('url')[1:-6] + "1")
        return error_string.split('url')[1:-6] + "1"


def upload_file(local_file_path: str, drop_box_file_name: str):
    drop_box_full_path = DROPBOX_ROOT_PATH + drop_box_file_name
    try:
        client.files_upload(open(local_file_path, "rb").read(), drop_box_full_path)
    except:
        print("File might already exists")

    try:
        print("[UPLOADED] {}".format(get_download_url_from_file(drop_box_full_path)))
        return get_download_url_from_file(drop_box_full_path)
    except:
        return ""
