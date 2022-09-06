import unittest
import json

from publish.OrderDetails import OrderDetails
from publish.lulu import get_access_token_json, client_id_sandbox, client_secret_sandbox, \
    get_job_details, get_line_items, submit_full_order, get_api_key, submit_order_with_payload, \
    client_id, client_secret, lulu_api_url, create_order_with_line_items, sandbox_api_url


def get_partial_payload():
    return """
{ "external_id": "RETHINK_YEARBOOKS", 
             "line_items" : [
             {
                            "title": "Naunidh Dhamija",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1-5tjILq5tYMP0WolDisxpF6iGR6O2ue9?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1xJhWiApQLFFA39iryZVYMm7RUwyng7Hm?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
            },
             {
                            "title": "J0008_Adventureland Room Copy",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1cOPSdtmdV9X4JBvZ147q5FjtSK9XT1iQ?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1JKD13RIfXHOn8CXVe34yaFu5lYi05riu?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
            },
            {
                            "title": "J0008_Jungle Room Copy",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1IrcdEu8uDIuhzcY0GHuxchkxp5UF_Xxx?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1a4hfCmSvVG2m2waHcW9X2-dOTA2Nugnu?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
            },
            {
                            "title": "J0008_Ladybugs Room Copy",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1IrcdEu8uDIuhzcY0GHuxchkxp5UF_Xxx?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1kFIu7WjS7zQc0U_SI-BIGA5HivZtALpI?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
            }
        ,{
                            "title": "J0011_Laura Sun",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1QofdgbZNWk_iIjUX2bEtflp9QLjo8EJh?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/14BKorGN-oCxcLR-XapCM33t54k2sK5Gw?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "J0003_Delilah Llamas",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/13GxTytxEoLPldP7GvgbZRIQoUP5_BLwa?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1phTyAihGzecVkrXF3-eMowMvqdxw4w0z?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "J0013_Bryce Jaylen Tang",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1wZAW7IKRAhv9rEt4ViKkq_Qz-XJfGfA-?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/105ixzNTEWKen7QPveZfvP5wGqkcwXFXA?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "J0007_Ms.  Barbara",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1nKfA1BFeTVfftNyG7bVn6xjIw7IA2zPU?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/18JXbJsQCQ-CF8mkqbjAJyrZ0Tsba7AIV?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10034_Advik Gowda",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1tldJOR1ypOEiYuZMyBzhKRX3P4Mz3L8o?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/15GtCeUc0tYrYGTHZkaY4A4HBhS9Qp7jP?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "J0010_Ryan Yuan",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1tsOcoxOPl2S7v6aGfB1nhy77d0qGjO-1?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1YWhWxE8ooONSAyNz9v_BYvK3W-LiDt-5?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "J0004_Sunshine Room Copy",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1jGWNzdyyDn_sips2Zri2SCI84Ri41dtf?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1NlvZMmijx628qZJMgR9ogeFp6YDXlr-v?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        },
                        {
                            "title": "Bryan - Classroom Betz",
                            "pod_package_id": "0850X1100FCPREPB080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/15EXma4MWq7uWApLGMZMbQcelK7alptHx?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1R7PvWq5ga-GH1_xxRoFbQ6zafr-ZGkTj?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
                        ,{
                            "title": "Jordan - Classroom Betz",
                            "pod_package_id": "0850X1100FCPREPB080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/15EXma4MWq7uWApLGMZMbQcelK7alptHx?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1kQadN7pEaITgtKwWssMqAMOQOpWoy-Hw?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        },
                        {
                            "title": "Victor - Classroom K Anderson",
                            "pod_package_id": "0850X1100FCPREPB080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1QuxNiicLdjg-6uG4s5Okvw4r55J-oqPM?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/12NC-AziCrMkMLR-YYqiEqtf4Oe5UsWfD?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        },{
                            "title": "Yamileth Classroom 4 Herron",
                            "pod_package_id": "0850X1100FCPREPB080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1weuCsDd9h4Srr1RhPm0bxKv-AsrUAHD6?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1qMnJGQfBZH_G7IQAKt0vnoHASIBlBidQ?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ] ,
            "shipping_option_level": "PRIORITY_MAIL",
            "contact_email": "rethinkyearbooks@gmail.com",
            "shipping_address": {
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
}
           }
     """


def get_one_item_payload():
    return """
    { "external_id": "RETHINK_YEARBOOKS", 
             "line_items" : [
             {
                            "title": "Monticello Proof Hard Cover",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                                                
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1FVgsYrHKE8u8CNTijFibFNsJ0P_EeZvF?alt=media&key=AIzaSyCUZS65rFygNfyws8bhv9wKeRDukn0niRk"
                            },
                            "cover": {
                                "source_url": "https://drive.google.com/uc?export=download&id=1FVr5PyfHuMdglGMOGhtEWQWh_UjQOOi2"
                            }
            }
            ],
            "shipping_option_level": "PRIORITY_MAIL",
            "contact_email": "rethinkyearbooks@gmail.com",
            "shipping_address": {
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
            
    }
    }
    """


def get_full_payload():
    return """ 
    { "external_id": "RETHINK_YEARBOOKS", 
             "line_items" : [{
                            "title": "MC0002_Ashley Mak",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/17uVMMhDVIA9N0YSVz33q_KLWaK9h2TOq?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1a6poFfJxIolF-5HjV783cXWp1loZ8edI?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10135_Enzo Lam",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1asvHZrCBmYzvEg4fuz-KvGR1IFkIfeca?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1_9YwgKNPBUY38qCa9U-dqogzdfLcMzBw?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "MC0005_Rachel Sun",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1DohgDubAozPlNNU9a6tk7hZ4TqIGoXRa?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1FejMoIDRBa1d2RCfLeiMCvkNf0OrW2jM?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10026_Srivardhan Srinivasan",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1bh5rqwF8El-24ZyjOvHyUp4N16wjsB-S?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1e8rVoQrME9t03CCKnBcYdTkXBHdjQbby?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10029_Zoey Nuoyi Li",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1r8QiSWrAfeb7RY9wVuPX_zqt4sLuIMq6?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1_Prk6vRS7MvJegTpMjT91zQm_c32bpDd?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "MC0001_Ada Sun",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/11MoY7aUb8pacipCEK6PA0AuwMNKAD1YF?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/18D643_WqdJfoE-U-t0MAjm6kqFSCYx6R?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10036_Amulya Sanaga",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1ryxdrxWzee3aziMSp4oxddQqJGc-i3x0?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1TL-rYnG5-Qdcs6qUXHqg0OIW9CqR3piq?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10193_Daniel Luo",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1_NzoxjtxvfIYW4qZ67cjyxXtV6LN-tXu?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1VzBDF0UEo5pkYsGIjOB8lHYA2i7MSp7b?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "MC0004_Jackson Walker",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1V50wjMIZ9s8rX0-m0x3DxQD_r6adMDfu?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1gi7bqimX4u8WqSprFT9_G0y9H8NFV-3x?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10033_Kaiya de Qhoury",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1mBm0Acs5MShU-jz6VH9GNL8y0CPgNAXM?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1EhtJkyyiiYTT1bcaUL7fzZGNuZF5RtTX?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10126_Kiki Quan",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1PlRv-p__fzanLpbTD972g72DWKFHgL2R?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1uX8GBI5aooYRa4XGIf5wLxiGBYGP--kc?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10037_Lucas Liu",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1Q7YVcHfPeWmpuJouH-ISJGYDOTeFuLt3?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1xxJ19VXOQB6DLXk0bq7v6jLOn-fpoiJp?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10192_Noble Lund",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1C6iYaWrjjNasUKxYrriT-0J9UdGORvef?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1Ll1vkGXIO6zg0l0sprj7aqOqeg8ZuKGB?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10134_Vera Choudhury",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1GSx6eTZCNp0XHYCTBTqeJZ1ysm_G6PPK?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1-if3FFT3k-TyEzWdGaV9f4Cz1nXEyQ0t?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "MC008_Evan Leung",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/19zbmzX9jKgFpMZTy8IEq36mkj7Q6xm_4?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1c3KSnNQR2C9isG1j4UW13ja3MgYgH5NW?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10107_Shuyi Jia",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1zHvo2Vios-IkhUV8UWmkddGW1mFl_4Y8?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1L-ufCikPNOLAHmL7EE5Mty1WasUS3EIF?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10017_Vyaas Avali",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1RsAjxW_oxow1V5Z5vFvlYVZ6DtbljbqG?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1J-74DBNAdo_--dxDtLz9Hdlti__Zw4GO?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10002_Yi-Bo Maksim Liu",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1jAYAQqp_x-O6awGhx1yrKki55Yv2Vb2z?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1sTzFjZ3JycYeolG-zyZuGw3H_3abw-9O?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10023_Aahana Namjoshi",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1ddmz5UI-9hGN7_ot5-PDAxePATGFqxXu?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1OwJpxvRjiZWMhvWWIYBD9sr4gmt7tHEP?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "MC0003_Elliana Walker",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/188Su9IbgD-sHVAudn2fyLSgpX7M-_gpE?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1Tp8WdvbZD2PkUSg_ZomaTR_U4eBMW_A_?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "MC0006_James Fishpaw",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1uOwN07gqRyMvxmjF4QQerxU1r-MW2x5C?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1Y2v1Ea_QaMq1sUxktBW3fsoIAz4gH3z3?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10022_Krish Dholaria",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1VxBwaoMpLEhgFQQAOcPuYmfdyjM_uVbO?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1rkftLxPZS1eViq6aQTy5rRHq-2wqDxSl?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10033_1_Ronin de Qhoury",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1F83B0uQS6y8NHSku_98krwFFQF2oqyKa?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1wX4x2wIbdF2MRs5jG2PmdjIdC-Vq0XZb?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10136_Sarah Lam",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1rBEHfzaEiDOVUV4EQ3cAZTyMiw08zTYQ?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1LuhMCQWAInLHe-Xm3QJSBnlDU5-VUpfd?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10106_Mia Lee",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/15fsNC4jKyii4G8sPZtz472tbQP4CoOWk?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1cYHcAmG0A6m_Qctfk37u2FrsUy9L0Kw6?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10054_Mira Nanduri Kale",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1xjp9cwJKg4tk-ak5WRZwnyFFsQ5JAiTI?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/15-Nf-3IoOk8s4KSPfYFozmLzqjHLcWKI?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10012_Reesha Raja",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1QxPFKmyfIlBLQia0VtMQ3Wxgi-a2Lnj-?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1ZFAl7_v-Zs2SIdDyrf8EGjUU0dDzB1T0?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10013_Remi Matsuda",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1K_8FEKtP6BI_6AbhYe9fYISZ3Z91NXZU?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1IC7sQc_xQ_e1I3NeJ2wS8mDJuf4Hxpy0?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10191_Siyuan (Eric) Ding",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1IdQim-AWRB8n91RzonkVuDbP4fz0Z8fQ?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1K07yfeD6Ce3Apot30-oXehHcUygFCrJj?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10034, 10133_Advik Gowda",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1HtfPL0ZEDGLmVQnoxOCk21KN5z1u9cqc?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1klxsPWWJVktlJJA9hNu34Q-rkk0aikyw?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10018_Agastya Avali",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1ZTel9Z8vqv9tlVV8Sss8GBKwXg2ZBvnW?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1eZmUTHVJkrccJVGyIeZUVBWIlWjzJies?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10145_Alexander Ding",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1whJz2PbNZTb61Huzv-ZLGMzp6zbQmHW0?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1yGwDW1UaEchZcHmdiI2vG_pksU_1SQyl?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10032_Caden Zhang",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1oe86LVAk6Rqv9oX98BW0cOl3IhoHl2WF?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1EZoSdp3KTmK8oRb9omNH91kz-zqrrZQb?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10003_Chengyu Li",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1QXqGCO5hYUs4pPAi9hIMisZFv4J7zStK?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1Xu7ZoRPdtWC7J3ZoIB6H6c8F28kuNOEo?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10006_Esther Mu",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1ZQFkiRJPyKQIBAaVzdgxW6xIooWa-taH?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1WnSLVzxyDsyjmx1IjBpkfiENsTZ9WOVk?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10024_Evelyn Ma",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1zxugILOkllZqBfcBjkdBbn5hVpvTChyq?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1q-pbl2E_bzFgawi2OGl-jQTzx-EEleO6?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10038_Grace Li",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1Oq1xAW4m0Fw1stsuOSsQa39P207ZXW-G?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1GGJUReTZM_5Ha2ySqVSQ55S34dXJWIk9?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10025_Madeline Chen",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1fdBddmlL4jWN2J2tIG3wctu8vYQxuvM3?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1mDFRQ6nlog-El_4Q9bNo2QjKu2hOzrvR?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10195_Mark Drobitho",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1g8v_ZGpZ8lH1s0sF0S3ed_54_Zb1ZTI0?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1GZiAxoYO8v-Q_Lh4unnAdF0iD3nBdqds?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10010_Martin Hu",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1ybOBfZJQZpGHr63OO_lYmURdv2uybw1A?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1zljjAKkIYUZwGL_YPY_HITw5b-AV9XU3?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10011_Matthew Yu",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1eSb4HVonK7xHUu3880R3GKPHlDhGotBV?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1KHWL0qCojIbuorGyEWuu2igsUzD2I-E6?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10016_Nayna Sidharth Aneja",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/16go-9_Y-ASZH-QfhcMkAm7qmT5Hg9hsx?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/10Pqdh-sSy3tk7WFWfse5l7A3WGwCQmSK?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10131_Ryan Li",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1xO7hxKiQRuMMPsZcT7DOKmufq1ZQT8Tx?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/17aINTtXqodHdN4VdHvNWNAQ5nCcQ3OCE?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10027_Ryan Yu",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1MH4MwqKmj3lfLg56z7USEQlcub2sDOB6?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1mwABqt4Y7NCZ14FTcGmP_kyJZKa5GlgF?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10014_Shivank Jithin",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1KEagIYHBEQCrTdLW1zvKS_Y43W1AVmz5?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/182uJbgFvM0dzFU9WmztrbbbrE1LKMx6m?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10009, 10110_Sophie Wu",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1_KeRCRiCyvlr-ryItiIHWMWG8XME6uLG?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/12cLXjk-3N4toFDKbjlSlpyVCf4QKhB5A?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10020_Tejaswin Kumar Satish",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/13jyealaleiVz-WNQiGDYJOUxuqkxK9BJ?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1qmFVlTZNBvqlzks7y_cUmbGAMZ9DOLY6?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ,{
                            "title": "10019_Tingyu Deng",
                            "pod_package_id": "0850X1100FCPRECW080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1Gstrm0DTkb7vTF44mYrQ6Smo5kn8NTkS?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            },
                            "cover": {
                                "source_url": "https://www.googleapis.com/drive/v3/files/1F0qat-phZ7kuKEdqMef8_vezGQnBVd2Z?alt=media&key=AIzaSyDC3t9lOmRPIootIOX0FiT31to6oPyVnEc"
                            }
                        }
        ] ,
            "shipping_option_level": "PRIORITY_MAIL",
            "contact_email": "rethinkyearbooks@gmail.com",
            "shipping_address": {
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
}
}

    """


def get_five_items_order():
    return """
    { "external_id": "RETHINK_YEARBOOKS", 
             "line_items" : [
             {
                            "title": "Cash13_Yeilin Perez Santos",
                            "pod_package_id": "0850X1100FCPREPB080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://drive.google.com/uc?export=download&confirm=9iBg&id=1LGoAU6TsK_8_mJoZuJVt2DTPeN_F4qNI"
                            },
                            "cover": {
                                "source_url": "https://drive.google.com/uc?export=download&confirm=9iBg&id=1JgWycx53onUcuF7eh6HCenI9sNf5tb8d"
                            }
                        }
            ,{
                            "title": "10053_Theodore Joseph Cincotta",
                            "pod_package_id": "0850X1100FCPREPB080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://drive.google.com/uc?export=download&confirm=9iBg&id=1-GnsJUuonok_aWqb2eRdAYxcdEoowMUN"
                            },
                            "cover": {
                                "source_url": "https://drive.google.com/uc?export=download&confirm=9iBg&id=1PnpVjHSPw4cruNVJgVODWioAPfHrMZXo"
                            }
            }
            
            ,{
                            "title": "10102_Andre LeDoux",
                            "pod_package_id": "0850X1100FCPREPB080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://drive.google.com/uc?export=download&confirm=9iBg&id=1Q8-Sl5IYMrtAAp2L0TzXf-0tu7UX7JmI"
                            },
                            "cover": {
                                "source_url": "https://drive.google.com/uc?export=download&confirm=9iBg&id=1TbEnoHcfgsX08HdMBU22jXnW6VfEqF0k"
                            }
            },
            {
                            "title": "Cash1_Samuel Gavino Tahuiton",
                            "pod_package_id": "0850X1100FCPREPB080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://drive.google.com/uc?export=download&confirm=9iBg&id=1Z5iZQzXDBT8tFl-SCdbI3qkHMzf8WygQ"
                            },
                            "cover": {
                                "source_url": "https://drive.google.com/uc?export=download&confirm=9iBg&id=1zwo6q2gL8Ae1pmvVbkDI_cqpBaFMN9Je"
                            }
            },
            {
                            "title": "10089_Kevin George Maquin",
                            "pod_package_id": "0850X1100FCPREPB080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://drive.google.com/uc?export=download&confirm=9iBg&id=1kgYBrvYVs_JBnhPmyuqBYXU1tjk0kS9v"
                            },
                            "cover": {
                                "source_url": "https://drive.google.com/uc?export=download&confirm=9iBg&id=1MPTbUEJLluIs7gMCHt0rGIekEyf2Tikd"
                            }
                        },
                        {
                            "title": "10055_Evie Smith",
                            "pod_package_id": "0850X1100FCPREPB080CW444GXX",
                            "quantity": 1,
                            "interior": {
                                "source_url": "https://drive.google.com/uc?export=download&confirm=9iBg&id=1lPwBNq3B8AXZ3LMWEEMaDAquEJNsHMjX"
                            },
                            "cover": {
                                "source_url": "https://drive.google.com/uc?export=download&confirm=9iBg&id=1uhLjY1l1-b7s3LgfAzZ1bPsuWbT2zibY"
                            }
                        }
        ] ,
            "shipping_option_level": "PRIORITY_MAIL",
            "contact_email": "rethinkyearbooks@gmail.com",
            "shipping_address": {
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
}
}
"""


class LuluIntegrationTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        print('BasicTest.__init__')
        super(LuluIntegrationTests, self).__init__(*args, **kwargs)

    def test_line_item(self):
        cover_url = "https://drive.google.com/file/d/1Y3y1GlcY4n120ERg_PU0ISNbiTnK1Rn9/view?usp=sharing"
        interior_url = "https://drive.google.com/file/d/1GpzDaNbea-aZcHFMzb-HvzP8isxIfYr5/view?usp=sharing"
        first_item = OrderDetails("1", "0827X1169FCPRELW060UW444MNG", interior_url, cover_url)

        json_item_str = first_item.get_lulu_line_item()
        assert ("0827X1169FCPRELW060UW444MNG" == json.loads(json_item_str)["pod_package_id"])

    def test_get_line_items(self):
        cover_url = "https://drive.google.com/file/d/1Y3y1GlcY4n120ERg_PU0ISNbiTnK1Rn9/view?usp=sharing"
        interior_url = "https://drive.google.com/file/d/1GpzDaNbea-aZcHFMzb-HvzP8isxIfYr5/view?usp=sharing"
        first_item = OrderDetails("1", "0827X1169FCPRELW060UW444MNG", interior_url, cover_url)
        second_item = OrderDetails("2", "0827X1169FCPRELW060UW444MNG", interior_url, cover_url)

        order_items = [first_item, second_item]

        json_items_str = get_line_items(order_items)
        print(json_items_str)

    def test_get_api_key(self):
        print(get_api_key("../api_key"))

    def test_create_all_print_jobs(self):
        cover_url = "https://www.googleapis.com/drive/v3/files/1PnpVjHSPw4cruNVJgVODWioAPfHrMZXo?alt=media&key=AIzaSyCUZS65rFygNfyws8bhv9wKeRDukn0niRk"
        interior_url = "https://www.googleapis.com/drive/v3/files/1-GnsJUuonok_aWqb2eRdAYxcdEoowMUN?alt=media&key=AIzaSyCUZS65rFygNfyws8bhv9wKeRDukn0niRk"

        print("Interior url %s" % interior_url)

        first_item = OrderDetails("1", "Softcover")
        first_item.interior_pdf_url = interior_url
        first_item.cover_url = cover_url
        first_item.child = "TestChild2"

        order_items = [first_item]
        for i in range(10):
            new_order = OrderDetails("%s" % i, "Softcover")
            new_order.interior_pdf_url = first_item.interior_pdf_url
            new_order.cover_url = first_item.cover_url
            new_order.wix_order_id = str(i)
            new_order.child = "TestChild1"
            order_items.append(new_order)

        response = submit_full_order(order_items)

        print(response.text)

    def test_get_access_token(self):
        access_token = get_access_token_json(client_id, client_secret, lulu_api_url)
        assert (access_token['expires_in'] == 3600)

    def test_get_job_details(self):
        created_job_id = self.test_create_print_job()
        self.test_job_details(created_job_id)

    def test_job_details(self, id):
        get_job_details(id)

    def test_job_details_for(self):
        get_job_details(client_id, client_secret, lulu_api_url, "856193")

    def test_submit_one_order(self):
        payload = get_one_item_payload()
        response = submit_order_with_payload(client_id, client_secret, lulu_api_url, payload)
        print(response.text)

    def test_submit_full_order(self):
        payload = get_full_payload()
        response = submit_order_with_payload(client_id, client_secret, lulu_api_url, payload)
        print(response.text)

    def test_submit_orders_in_multiple_batches(self):

        payload = get_full_payload()
        payload_json = json.loads(payload)

        line_items = payload_json['line_items'][:4]

        order_payload = create_order_with_line_items(str(line_items).replace("'", "\""))
        # print(order_payload)
        response = submit_order_with_payload(client_id_sandbox, client_secret_sandbox, sandbox_api_url, order_payload)
        print(response.text)

    def test_submit_partial_order(self):
        payload = get_partial_payload()
        response = submit_order_with_payload(client_id, client_secret, lulu_api_url, payload)
        print(response.text)

    def test_submit_five_item_order(self):
        payload = get_five_items_order()
        response = submit_order_with_payload(client_id, client_secret, lulu_api_url, payload)
        print(response.text)
