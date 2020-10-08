#!/usr/bin/python
import json
import os
import time

import bwi
from mailjet_rest import Client


NEXT_BEE = 'alert_signup'


def callback_customer(data):
    t = time.process_time()
    print(data)
    data = json.loads(data)
    print(data)
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
    print(data)
    print(data['email'])
    bwi.logs.info("Adding " + str(data['email']) + " to the list id=" + str(listid))
    if 200 <= result.status_code <= 299:
        data['status'] = "SUCCESS"
        bwi.logs.info(str(data['email']) + " has been added to the list")
        bwi.metrics.counter("add_to_ma", 1)
    else:
        data['status'] = "FAIL"
        bwi.logs.error(str(data['email']) + " can't be added to the list : " + str(result))
        bwi.metrics.counter("fail_add_to_ma", 1)
    elapsed_time = time.process_time() - t
    bwi.metrics.store("add_to_ma_time", elapsed_time)
    return json.dumps(data)


if __name__ == '__main__':
    callback_customer(
        '{"email": "martin_e@etna-alternance.net", "first_name": "Antoine"}')
