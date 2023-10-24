import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
import datetime

from dotenv import load_dotenv  # pip install python-dotenv
# -------------------
from flask import Flask, request
import requests
import openai
import os
from system import system_message

# Set up your OpenAI API key
openai.api_key = 'xxxxx'

app = Flask(__name__)

# Verification token for WhatsApp integration
VERIFY_TOKEN = "farhan205"

def send_msg(msg, receiver_number):
    headers = {
        'Authorization': 'Bearer EAAOp52EX6kgBO7GFrupNzaecHZBEswM0sJIptzZAYUdChYmW5ZBJlY5M1uEqUYlHqxTThwGRPY2z8bljv6rdztRVsgUnDU11G7YWdjfU4veOl2L1bMFW4hRvn4S01Vj0x0R7fT1j3fZBUXHuubbmqw1e37YGj1qKnicXExXY7Why74i5ZAbShip1xl1g9iTk6fpfKuQtGg1RgPypyN7Y29hvNQlG7ZC8VT6Hrrqcpsfljd4QzM',
    }
    json_data = {
        'messaging_product': 'whatsapp',
        'to': receiver_number,
        'type': 'text',
        "text": {
            "body": msg
        }
    }
    response = requests.post('https://graph.facebook.com/v17.0/132277916635812/messages', headers=headers, json=json_data)
    print(response.text)


@app.route('/receive_msg', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        # Handle the subscription verification request
        hub_mode = request.args.get("hub.mode")
        hub_challenge = request.args.get("hub.challenge")
        if hub_mode == "subscribe" and hub_challenge:
            hub_verify_token = request.args.get("hub.verify_token")
            if hub_verify_token == VERIFY_TOKEN:
                return hub_challenge, 200
            else:
                return "Verification token mismatch", 403
    elif request.method == 'POST':
        # Handle incoming WhatsApp messages
        res = request.get_json()
        print(res)
        try:
            if res['entry'][0]['changes'][0]['value']['messages'][0]['id']:
                chat_gpt_input = res['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
                if chat_gpt_input == "hello":
                    user_name = res['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
                    wa_id = res['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
                    #   send_email(subject="Chatbot",name="Farhan",receiver_email="fafridi047@gmail.com" ,user_name = user_name , wa_id = wa_id)
                    def send_notify(msg="this is person is interested", r_number="+923101284817" , user_name = user_name   , wa_id = wa_id ):
                            headers = {
                                'Authorization': 'Bearer EAAOp52EX6kgBO7GFrupNzaecHZBEswM0sJIptzZAYUdChYmW5ZBJlY5M1uEqUYlHqxTThwGRPY2z8bljv6rdztRVsgUnDU11G7YWdjfU4veOl2L1bMFW4hRvn4S01Vj0x0R7fT1j3fZBUXHuubbmqw1e37YGj1qKnicXExXY7Why74i5ZAbShip1xl1g9iTk6fpfKuQtGg1RgPypyN7Y29hvNQlG7ZC8VT6Hrrqcpsfljd4QzM',
                            }
                            json_data = {
                                'messaging_product': 'whatsapp',
                                'to': r_number,
                                'type': 'text',
                                "text": {
                                    "body": msg + user_name + wa_id
                                }
                            }
                            response = requests.post('https://graph.facebook.com/v17.0/132277916635812/messages', headers=headers, json=json_data)
                            print(response.text)
                    send_notify(msg="this is person is interested", r_number="+923101284817" ,user_name = user_name ,wa_id =wa_id )
                      
                   
                   

# ---------------------------------------------------------------------------
                
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": system_message},
                              {"role": "user", "content": chat_gpt_input}],
                    max_tokens=50
                )
                response = completion['choices'][0]['message']['content']
                
                print("ChatGPT Response =>", response)
                receiver_number = res['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
                send_msg(response, receiver_number)
                # send_notify(response, receiver_number)
        except Exception as e:
            print("Error:", e)

    return '200 OK HTTPS.'


# Code for email notification 


# print("lllllllllllllllllllllllllllllllllllllllllllllllllllllll")
# PORT = 587  
# EMAIL_SERVER = "smtp.gmail.com"  # Adjust server address, if you are not using @outlook
# current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
# print('send email function 3 below')
# envars = current_dir / ".env"
# load_dotenv(envars)
# print('send email function 4 below')
# # Read environment variables
# sender_email = "hassanqureshi700@gmail.com"
# password_email = "ytce cpjx fyzz pfoz"
# print('send email function 1 below')
# def send_email(subject, receiver_email, name , user_name , wa_id):
#                         # Create the base text message.
#                         msg = EmailMessage()
#                         msg["Subject"] = subject
#                         msg["From"] = formataddr(("Chatbot", f"{sender_email}"))
#                         msg["To"] = receiver_email
#                         msg["BCC"] = sender_email
#                         print('send email function 2 below')
#                         msg.set_content(
#                             f"""\
#                             {datetime.datetime.now().strftime('%d-%B-%Y (%I:%M %p)')}

#                             Dear {name}, How are you?
#                             This below person is interested to buy a property .please contact him ASAP.
#                             User Name : {user_name}
#                             Whats app Number : {wa_id}
#                             """
#                         )

#                         with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
#                             server.starttls()
#                             server.login(sender_email, password_email)
#                             server.sendmail(sender_email, receiver_email, msg.as_string())
#                         print('send email function 56 below') 


if __name__ == "__main__":
     
     app.run(debug=True)
