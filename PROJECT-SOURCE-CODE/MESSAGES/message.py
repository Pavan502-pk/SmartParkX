from twilio.rest import Client


def MESSAGE(number_plate,minutes,amount,rcvr):
    #Authentication

    account_sid = 'ACf91651b02641aba70168afc8629253f0'

    auth_token = 'be08a2ed1896dbd96c1ade7c359b322f'

    client = Client(account_sid, auth_token)

    np=number_plate
    td=minutes
    pd=amount
    symbol='+'
    pre=91
    receiver=f'{symbol}{pre}{rcvr}'

    #Sending SMS   =>High Cost ($1.13)  & Low Speed (1 min)
    #client.messages.create(body= f'Hey Hi ,You have been charged of {pd} rupees for your vehicle number {np} for parking your vehicle for {td} minutes  Thank You Visit Again.' , from_= '+18507559138' , to='+91 7337010225')

    #Sending Whatsapp SMS  =>Low Cost ($0.005)  &  High Speed (2 sec)
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=f'Hey Hi ,\n \n Please pay the charges of *{pd}* rupees for your vehicle number *{np}* for parking your vehicle for *{td}* minutes  by following QR code on the Screen \n \n Thank You Visit Again.',
    to=f'whatsapp:{receiver}'
    )
    

#MESSAGE("XYZ",47,87,7337010225)