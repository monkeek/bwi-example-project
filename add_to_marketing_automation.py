#!/usr/bin/python
import json
import os

import bwi
from mailjet_rest import Client


def callback_customer(data):
    data = (json.loads(data))
    api_key = os.environ.get('MAILJET_APIKEY')
    api_secret = os.environ.get('MAILJET_APISECRET')
    mailjet = Client(auth=(api_key, api_secret), version='v3')
    mjdata = {
        "Action": "addnoforce",
        'Contacts': [
            {
                "Email": data['email'],
                "Name": data['first_name']
            }
        ]
    }
    listid = os.environ.get('MAILJET_MA_LIST')
    result = mailjet.contactslist_managemanycontacts.create(data=mjdata,
                                                            id=listid)
    bwi.logs.info("Adding " + data['email'] + " to the list id=" + listid)
    if 200 <= result.status_code <= 299:
        bwi.logs.info(data['email'] + " has been added to the list")
    else:
        bwi.logs.error(
            data['email'] + " can't be added to the list : " + result)
    return data


if __name__ == '__main__':
    callback_customer(
        '{"email": "martin_e@etna-alternance.net", "first_name": "Antoine"}')
