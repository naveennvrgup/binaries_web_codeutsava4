import boto3

AWS_ACCESS_KEY_ID = 'AKIAYB5CEBDBDDL3JBVU'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION_NAME = 'eu-west-1'

client = boto3.client(
    'sns',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

response = client.publish(
    PhoneNumber='+918940073123',
    Message='this is a test bro',
)

print(response)


https://www.fast2sms.com/dev/bulk?authorization=J2dRIcPLHiO9GKXk0za4EjN8MACTxev3f7oysbYgWuQZUmVht5qGrktE2KzeT9VWg5nA4Db1y6CLmNP3&message=This is test message&language=english&route=p&numbers=8940073123&sender_id=FSTSMS
