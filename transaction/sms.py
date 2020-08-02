import http.client
from decouple import config
from django.http import HttpResponse
import requests

def send_sms(contact, message):
    print(contact, message, "called")

    url = "https://www.fast2sms.com/dev/bulk"
    querystring = {
        "authorization":"J2dRIcPLHiO9GKXk0za4EjN8MACTxev3f7oysbYgWuQZUmVht5qGrktE2KzeT9VWg5nA4Db1y6CLmNP3",
        "sender_id":"FSTSMS",
        "message":message,
        "language":"english",
        "route":"p",
        "numbers":str(contact)
    }

    headers = {
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)



#send_sms("7024901272", "It worked")