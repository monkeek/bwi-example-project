#!/usr/bin/python
import json
import os
import time

import bwi
from mailjet_rest import Client


START_BEE = True
NEXT_BEE = 'add_to_marketing_automation'


def callback_customer(data):
    t = time.process_time()
    data = (json.loads(data))
    api_key = os.environ.get('MAILJET_APIKEY')
    api_secret = os.environ.get('MAILJET_APISECRET')
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    mjdata = {
        'Messages': [
            {
                "From": {
                    "Email": "contact@bwi-project.com",
                    "Name": "Antoine de BWI"
                },
                "To": [
                    {
                        "Email": data['email'],
                        "firstname": data['first_name']
                    }
                ],
                "TemplateID": 1106753,
                "TemplateLanguage": True,
                "Subject": "Bienvenue dans la Hive",
                "Variables": {
                    "firstname": data['first_name']
                }
            }
        ]
    }
    result = mailjet.send.create(data=mjdata)
    bwi.logs.info("Sending signup email to " + data['email'])
    if 200 <= result.status_code <= 299:
        bwi.logs.info("Signup email has been sent to " + data['email'])
        bwi.metrics.counter("sent_signup_email", 1)
    else:
        bwi.logs.error("Signup email has not been sent to " + data['email'])
        bwi.metrics.store("error_signup_email", 1)
    elapsed_time = time.process_time() - t
    bwi.metrics.store("signup_time", elapsed_time)

    return json.dumps(data)


if __name__ == '__main__':
    # callback_customer('{"email": "antoine@visiblee.io", "first_name": "Antoine"}')
    callback_customer('{"email": "aroumo_v@etna-alternance.net", "first_name": "Vinod"}')
    callback_customer('{"email": "derouc_c@etna-alternance.net", "first_name": "Clovis"}')
    callback_customer('{"email": "rollan_t@etna-alternance.net", "first_name": "Thomas"}')
    callback_customer('{"email": "massar_t@etna-alternance.net", "first_name": "Théo"}')
