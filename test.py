from twilio.rest import Client



account_sid = 'ACe5540840f09d2c2fc9cabaa750c8d0e3'
auth_token = 'a0206af2ecdedbc0ebcbec894e7ec95e'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body=f''' Dear Sir/madam Your son/Daughter applied for leave from Jan. 22, 2021-Jan. 23, 2021''',
                     from_='(938) 300-4223',
                     to='+919449518420'
                 )




