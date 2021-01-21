from twilio.rest import Client



account_sid = 'ACe5540840f09d2c2fc9cabaa750c8d0e3'
auth_token = '7f92f516c66dee69d028791b5ab484f1'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body='''Yo I am priya from hampankatta manglore
                        I want to have SEX with you if you intrested Text me using this link:https://www.instagram.com/p/CEE8Fj4lfgK/
                        Iam waiting BABY😍😍😘😘 ''',
                     from_='(938) 300-4223',
                     to='+918277456837'
                 )




