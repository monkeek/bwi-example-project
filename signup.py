#!/usr/bin/python
import json
import os

import bwi
from mailjet_rest import Client


def callback_customer(data):
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
                        "Name": data['first_name']
                    }
                ],
                "Subject": "Bienvenue chez BWI.",
                "HTMLPart": "<h3>Bienvenue dans la hive !</h3><br/>May the "
                            "force bee with you!"
            }
        ]
    }
    result = mailjet.send.create(data=mjdata)
    bwi.logs.info("Sending signup email to " + data['email'])
    if 200 <= result.status_code <= 299:
        bwi.logs.info("Signup email has been sent to " + data['email'])
        bwi.metrics.store("sent_email", 1)
    else:
        bwi.logs.error("Signup email has not been sent to " + data['email'])
        bwi.metrics.store("error_email", 1)

    return data


if __name__ == '__main__':
    callback_customer(
        '{"email": "antoine@visiblee.io", "first_name": "Antoine"}')
