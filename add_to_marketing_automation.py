#!/usr/bin/python
def callback_customer(data):
    print("It's a good day, we've received a message in queue add_to_marketing_automation")
    print(data)
    print("Send it to queue billing now !")
    return data