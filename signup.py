#!/usr/bin/python
def callback_customer(data):
    print("It's a good day, we've received a message in queue signup")
    print(data)
    print("Send it to queue add_to_marketing_automation now !")
    return data