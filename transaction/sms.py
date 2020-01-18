import http.client
from decouple import config
from django.http import HttpResponse

def send_sms(contact, message):
    conn = http.client.HTTPSConnection("api.msg91.com")

    payload = '{ \"sender\": \"KISANI\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"'+message+'\", \"to\": [ \"'+str(contact)+'\" ] } ] }'

    headers = {
        'authkey': config('authkey'),
        'content-type': "application/json"
        }

    conn.request("POST", "/api/v2/sendsms?country=91", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    return HttpResponse('Registration successful!!!')