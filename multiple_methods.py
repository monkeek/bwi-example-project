#!/usr/bin/python
def toto(data):
    print("It's a good day, we've received a message in queue send_welcome_gift")
    print(data)
    print("Send it to queue result now !")
    return data

def callback_customer(data):
    return toto(data)
