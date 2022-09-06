import json

import requests

from publish.OrderDetails import OrderDetails

client_id_sandbox = '0f945822-ca71-413b-b986-d0037c7e0b05'
client_secret_sandbox = '89cc568b-44dd-477a-a0f4-0e1bd30f7ce5'
sandbox_api_url = "https://api.sandbox.lulu.com/auth/realms/glasstree/protocol/openid-connect/token"
sandbox_base_url = "https://api.sandbox.lulu.com/"
lulu_base_url = "https://api.lulu.com/"
lulu_api_url = "https://api.lulu.com/auth/realms/glasstree/protocol/openid-connect/token"

print_job_url = lulu_base_url + "print-jobs/"
job_details_url = lulu_base_url + "print-jobs/%s/"
sandbox_print_job_url = sandbox_base_url + "print-jobs/"


VARGAS_POD_ID = "0850X1100FCPREPB080CW444GXX"
LULU_MONTICELLO_POD_ID = "0827X1169FCPRELW060UW444GNG"
client_id = "4bae975e-030d-4da7-a320-c7e3441f4c41"
client_secret = "d03ac1bd-32b2-43ba-902c-bb838b37e4ce"


def get_api_key(filename):
    """ Given a filename,
        return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)


def get_access_token_json(client_id: str, client_secret: str, api_url: str = sandbox_api_url) -> str:
    data = {'grant_type': 'client_credentials'}
    access_token_response = requests.post(api_url, data=data, allow_redirects=False,
                                          auth=(client_id, client_secret))
    return access_token_response.json()


def __get_pod_package_id() -> str:
    """
    0827X1169: A4 Medium
    FC: full color
    STD: standard quality/ PRE: Premium Quality
    LW: linen wrap binding
    080CW444: 80# uncoated white paper with a bulk of 444 ppi
    M: matte cover coating
    N: navy colored linen
    G: golden foil stamping
    :return: Gives a predefined set LULU POD package id
    """
    return "0827X1169FCPRELW060UW444MNG"


def get_shipping_json() -> str:
    return """{
        "name": "Mudita Singhal",
        "organization":"Rethink Yearbooks",
        "street1": "1042 Waterbird Way",
        "city": "Santa Clara",
        "state_code": "CA",
        "country_code": "US",
        "postcode": "95051",
        "phone_number": "408-438-6825",
        "email" : "rethinkyearbooks@gmail.com",
        "is_business":true
    }"""


def get_line_items(student_books: [OrderDetails]) -> str:
    internal_line_items = ",".join([line_item.get_lulu_line_item() for line_item in student_books])
    return """ "line_items" : [""" + internal_line_items + "]"


def create_order_with_line_items(internal_line_items, external_id="RethinkYearbooks") -> str:
    line_items = """ "line_items" : [""" + internal_line_items[1:-1] + "]"

    data = """{ "external_id": "%s", 
                %s ,
                "shipping_option_level": "PRIORITY_MAIL",
                "contact_email": "rethinkyearbooks@gmail.com",
                "shipping_address": %s
               }""" % (external_id, line_items, get_shipping_json())
    return data


def create_order_payload(student_books: [OrderDetails], external_id="RethinkYearbooks") -> str:
    data = """{ "external_id": "%s", 
                %s ,
                "shipping_option_level": "PRIORITY_MAIL",
                "contact_email": "rethinkyearbooks@gmail.com",
                "shipping_address": %s
               }""" % (external_id, get_line_items(student_books), get_shipping_json())
    return data


def get_header(id, secret, api_url: str = sandbox_api_url) -> str:
    headers = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Authorization': 'Bearer %s' % get_access_token_json(id, secret, api_url)[
            'access_token'],
    }
    return headers


def submit_order_with_payload(id, secret, api_url, job_payload):
    headers = get_header(id, secret, api_url)

    response = requests.request('POST', print_job_url, data=job_payload, headers=headers)
    return response


def submit_full_order(student_books: [OrderDetails], id, secret, api_url, external_id="RethinkYearbooks"):
    job_payload = create_order_payload(student_books, external_id)
    return submit_order_with_payload(id, secret, api_url, job_payload)


def get_job_details(id, secret, api_url, lulu_job_id: str):
    url = job_details_url % lulu_job_id
    print(url)
    headers = get_header(id, secret, api_url)

    response = requests.request('GET', url, headers=headers)

    #print(response.text)
    lulu_output = json.loads(response.text)
    [print(str(line_item['title']) + "_" + str(line_item['status'])) for line_item in lulu_output['line_items']]

    return response.text


def main():
    from data.model.ModelCreator import get_tree_model
    import os
    import getpass

    corpus_base_dir = os.path.join('/Users', getpass.getuser(), 'GoogleDrive')
    output_base_dir = os.path.join('/Users', getpass.getuser(), 'YearbookCreatorOut')
    input_base_dir = os.path.join(corpus_base_dir, 'YearbookCreatorInput')
    yearbook_parameters = {'max_count': 12,
                           'db_file_path': os.path.join(input_base_dir, 'RY.db'),
                           'output_dir': os.path.join(output_base_dir, getpass.getuser()),
                           'corpus_base_dir': corpus_base_dir}

    treeModel = get_tree_model(yearbook_parameters, "VargasElementary")

    treeModel.foreach()