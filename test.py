import requests
from flask import Flask, request

rasa_url = 'http://localhost:5005'
chatwoot_url = 'http://localhost:3000'
chatwoot_bot_token = 'B5gU3CH687As1YjA8qXzR36u'


def send_to_bot(sender, message):
    data = {
        'sender': sender,
        'message': message
    }
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    r = requests.post(f'{rasa_url}/webhooks/rest/webhook',
                      json=data, headers=headers)
    return r.json()[0]['text']
def rasa():
    data = request.get_json()
    message_type = data['message_type']
    message = data['content']
    conversation = data['conversation']['id']
    contact = data['sender']['id']
    account = data['account']['id']

    if(message_type == "incoming"):
        bot_response = send_to_bot(contact, message)
        # create_message = send_to_chatwoot(
        #     account, conversation, bot_response)
    return bot_response
rasa()