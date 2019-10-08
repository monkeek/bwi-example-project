#!/usr/bin/python
def callback_customer(data):
    print("It's a good day, we've received a message in queue billing")
    print(data)
    print("Send it to queue send_welcome_gift now !")
    return data