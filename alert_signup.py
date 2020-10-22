#!/usr/bin/python
import json
import os
import time

import bwi
from mailjet_rest import Client


NEXT_BEE = 'result'

ALERT_EMAIL = os.environ.get('CUSTOMER_SUCCESS_MAIL')

def callback_customer(data):
    t = time.process_time()
    tmp_data = json.loads(data)
    if tmp_data['register_status'] != "SUCCESS":
        return data
    data = tmp_data
    api_key = os.environ.get('MAILJET_APIKEY')
    api_secret = os.environ.get('MAILJET_APISECRET')
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    mjdata = {
        'Messages': [
            {
                "From": {
                    "Email": "contact@bwi-project.com",
                    "Name": "BWI - Signup notifications"
                },
                "To": [
                    {
                        "Email": str(ALERT_EMAIL)
                    }
                ],
                "TemplateID": 1107138,
                "TemplateLanguage": True,
                "Subject": "Une nouvelle abeille s'est inscrite",
                "Variables": {
                    "email": data['email'],
                    "firstname": data['first_name']
                }
            }
        ]
    }
    result = mailjet.send.create(data=mjdata)
    bwi.logs.info("Sending alert signup email to " + str(ALERT_EMAIL))
    if 200 <= result.status_code <= 299:
        data['register_status'] = "SUCCESS"
        bwi.logs.info("Alert signup email has been sent to " + str(ALERT_EMAIL))
        bwi.metrics.store("sent_email", 1)
        bwi.metrics.counter("alert_signup", 1)
    else:
        data['register_status'] = "ERROR_ALERT"
        bwi.logs.error("Alert signup email has not been sent to " + str(ALERT_EMAIL))
        bwi.metrics.store("error_email", 1)
        bwi.metrics.counter("fail_alert_signup", 1)
    elapsed_time = time.process_time() - t
    bwi.metrics.store("alert_signup_time", elapsed_time)
    return json.dumps(data)


if __name__ == '__main__':
    callback_customer(
        '{"email": "aroumo_v@etna-alternance.net", "first_name": "Vinod"}')
