
# from flask import Flask, request
# import requests
# import openai
# import os
# from system import context

# openai.api_key=os.getenv('OPENAI_API_KEY')

# app = Flask(__name__)
 
# def send_msg(msg,receiver_number):

#    headers = {
#        'Authorization': 'Bearer EAAOp52EX6kgBOZB5VwBlZAjv50RmupsYU068Y9rRGeZBjWj80tWWHU0ZBBaCN0n2jOWhMGVbqeOZBHwnfXJ8Cm7VkXsHHOHHK0pnbjenmNt1eAzbRqwZBnqdewvFCpiE0Hdc4kZCgBysBI37jcYzQi6louXwZCkIUUZB1eOyZA3InEQ8MoQ5cZBD48dcS419fafbSnfv3ZAbXaVv20xxYjsM1GVaZCv82IlXDd3oZBcJ9yIK0ZBM0GnWXZCX',
#    }
#    json_data = {
#        'messaging_product': 'whatsapp',
#        'to': receiver_number,
#        'type': 'text',
#        "text": {
#            "body": msg
#        }
#    }
#    response = requests.post('https://graph.facebook.com/v17.0/132277916635812/messages', headers=headers, json=json_data)
#    print(response.text)
 

# @app.route('/receive_msg', methods=['POST','GET'])
# def webhook():
#    res = request.get_json()
#    print(res)
#    try:
#        if res['entry'][0]['changes'][0]['value']['messages'][0]['id']:
#             chat_gpt_input=res['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
#             completion = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role":"user","content":context},
#                 {"role": "user", "content": chat_gpt_input}],
#                 max_tokens=50
#             )
#             response = completion['choices'][0]['message']['content']
#             print("ChatGPT Response=>",response)
#             receiver_number=res['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
#             send_msg(response,receiver_number)
#    except:
#        pass
#    return '200 OK HTTPS.'
 
  
# if __name__ == "__main__":
#    app.run(debug=True)


# _____________________________________________________________________________________________________


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
import re
# Set up your OpenAI API key
openai.api_key = 'XXXX'

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
                user_text = chat_gpt_input

                if re.search(r'\bcontact\b', user_text, flags=re.IGNORECASE):
                    user_name = res['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
                    wa_id = res['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
                    notification_message = f"""\
                            Dear Waqas Ali, hope you are fine!\
                            This below person is interested to buy a property. Please contact him ASAP. 
                            \
                            Name : {user_name}\
                            WhatsApp Number : {wa_id}\
                            """
                    #   send_email(subject="Chatbot",name="Farhan",receiver_email="fafridi047@gmail.com" ,user_name = user_name , wa_id = wa_id)
                    def send_notify(msg=notification_message, r_number="+923101284817"):
                            headers = {
                                'Authorization': 'Bearer EAAOp52EX6kgBO7GFrupNzaecHZBEswM0sJIptzZAYUdChYmW5ZBJlY5M1uEqUYlHqxTThwGRPY2z8bljv6rdztRVsgUnDU11G7YWdjfU4veOl2L1bMFW4hRvn4S01Vj0x0R7fT1j3fZBUXHuubbmqw1e37YGj1qKnicXExXY7Why74i5ZAbShip1xl1g9iTk6fpfKuQtGg1RgPypyN7Y29hvNQlG7ZC8VT6Hrrqcpsfljd4QzM',
                            }
                            json_data = {
                                'messaging_product': 'whatsapp',
                                'to': r_number,
                                'type': 'text',
                                "text": {
                                    "body": msg
                                }
                            }
                            response = requests.post('https://graph.facebook.com/v17.0/132277916635812/messages', headers=headers, json=json_data)
                            print(response.text)
                    send_notify()
                      
                   
                   

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

# ________________________________________________________________________________________________________

# from flask import Flask, request
# import requests
# import openai
# from system import system_message

# app = Flask(__name__)

# # Set up your OpenAI API key
# openai.api_key = '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'

# VERIFY_TOKEN = "farhan205"

# # Initialize context with system message
# context = [{'role': 'system', 'content': system_message}]

# # def send_msg(msg, receiver_number):
# #     headers = {
# #         'Authorization': 'Bearer EAAOp52EX6kgBOZB5VwBlZAjv50RmupsYU068Y9rRGeZBjWj80tWWHU0ZBBaCN0n2jOWhMGVbqeOZBHwnfXJ8Cm7VkXsHHOHHK0pnbjenmNt1eAzbRqwZBnqdewvFCpiE0Hdc4kZCgBysBI37jcYzQi6louXwZCkIUUZB1eOyZA3InEQ8MoQ5cZBD48dcS419fafbSnfv3ZAbXaVv20xxYjsM1GVaZCv82IlXDd3oZBcJ9yIK0ZBM0GnWXZCX',
# #     }
# #     json_data = {
# #         'messaging_product': 'whatsapp',
# #         'to': receiver_number,
# #         'type': 'text',
# #         "text": {
# #             "body": msg
# #         }
# #     }
# #     response = requests.post('https://graph.facebook.com/v17.0/132277916635812/messages', headers=headers, json=json_data)
# #     print(response.text)

# def send_msg(msg, receiver_number):
#     headers = {
#         'Authorization': 'Bearer EAAOp52EX6kgBO7GFrupNzaecHZBEswM0sJIptzZAYUdChYmW5ZBJlY5M1uEqUYlHqxTThwGRPY2z8bljv6rdztRVsgUnDU11G7YWdjfU4veOl2L1bMFW4hRvn4S01Vj0x0R7fT1j3fZBUXHuubbmqw1e37YGj1qKnicXExXY7Why74i5ZAbShip1xl1g9iTk6fpfKuQtGg1RgPypyN7Y29hvNQlG7ZC8VT6Hrrqcpsfljd4QzM',
#     }
    
#     # Check if the user's message contains any of the keywords
#     keywords = ["video", "audio", "image", "document"]
#     found_keyword = None

#     for keyword in keywords:
#         if keyword in msg.lower():
#             found_keyword = keyword
#             break  
    
#     if found_keyword == "video":
#         json_data = {
#             "messaging_product": "whatsapp",
#             "recipient_type": "individual",
#             "to": receiver_number,
#             "type": "video",
#             "video": {
#                 "link" : "https://drive.google.com/uc?id=1hnCzLmc9szELfTmd7yooInIPWUF9wYAs&download=Habibi_output.mp4"
#                 }
#             }
#     elif found_keyword == "audio":
#         json_data = {
#                     "messaging_product": "whatsapp",
#                     "recipient_type": "individual",
#                     'to': receiver_number,
#                     "type": "audio",
#                     "audio": {
#                         "link": "https://drive.google.com/uc?id=1wJ0B41alzAbRZsYYDiuRqinO9QrgekGB&download=Credit.ogg"
#                     }
#                 }
#     elif found_keyword == "image":
#         json_data = {
#             "messaging_product": "whatsapp",
#             "recipient_type": "individual",
#             "to": receiver_number,
#             "type": "image",
#             "image": {
#                 "link": "https://drive.google.com/uc?id=1QA7ajCGUaq_TFlqGb1HlU4vihtPsw2jp&download=Habibi.png"
#                 }
#             }
#     elif found_keyword == "document":
#         json_data = {
#             "messaging_product": "whatsapp",
#             "recipient_type": "individual",
#             "to": receiver_number,
#             "type": "document",
#             "document": {
#                 "link": "https://drive.google.com/uc?id=15TxQv4-eZaJIt2Q9oQeW-riTGxGGLpcr&download=Empire_Suites.pdf"
#                 }
#             }
#     else:
#         # If no keyword is found, send a text response
#         json_data = {
#             "messaging_product": "whatsapp",
#             "recipient_type": "individual",
#             "to": receiver_number,
#             "type": "text",
#             "text": {
#                 "body": msg
#             }
#         }

#     response = requests.post('https://graph.facebook.com/v17.0/132277916635812/messages', headers=headers, json=json_data)
#     print(response.text)

# def get_completion_from_messages(messages, model="gpt-3.5-turbo"):
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0.2,
#     )
#     return response.choices[0].message["content"]

# def process_user_message(prompt):
#     user_message = {'role': 'user', 'content': prompt}
#     context.append(user_message)
#     response = get_completion_from_messages(context)
#     context.append({'role': 'assistant', 'content': response})
#     return response

# @app.route('/receive_msg', methods=['POST', 'GET'])
# def webhook():
#     if request.method == 'GET':
#         hub_mode = request.args.get("hub.mode")
#         hub_challenge = request.args.get("hub.challenge")
#         if hub_mode == "subscribe" and hub_challenge:
#             hub_verify_token = request.args.get("hub.verify_token")
#             if hub_verify_token == VERIFY_TOKEN:
#                 return hub_challenge, 200
#             else:
#                 return "Verification token mismatch", 403
#     elif request.method == 'POST':
#         res = request.get_json()
#         try:
#             if res['entry'][0]['changes'][0]['value']['messages'][0]['id']:
#                 chat_gpt_input = res['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
#                 response = process_user_message(chat_gpt_input)
#                 receiver_number = res['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
#                 send_msg(response, receiver_number)
#         except Exception as e:
#             print("Error:", e)

#     return '200 OK HTTPS.'

# if __name__ == "__main__":
#     app.run(debug=True)

# -------------------------------------------------------------------------------------


# from flask import Flask, request
# import requests
# import openai
# from system import system_message

# # Set up your OpenAI API key
# openai.api_key = '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'

# app = Flask(__name__)

# # Verification token for WhatsApp integration
# VERIFY_TOKEN = "farhan205"

# # 

# # Define keyword-to-data mapping
# keyword_to_data = {
#     "video": {
#         "type": "video",
#         "link": "https://drive.google.com/uc?id=1ld5soq_oJ3OxQtHjdrI8FLWz_4NPzQ3D&download=Sample.mp4",
#         "caption": "Check out this amazing video!",
#     },
#     "image": {
#         "type": "image",
#         "link": "https://drive.google.com/uc?id=1PwmvEO78EVTjloaBn0XshiD0ZL92tu9c&download=cgd.jpeg",
#         "caption": "Check out this amazing project!",
#     },
#     "document": {
#         "type": "document",
#         "link": "https://drive.google.com/uc?id=15TxQv4-eZaJIt2Q9oQeW-riTGxGGLpcr&download=Empire_Suites.pdf",
#         "caption": "Here are all the details in the given document!",
#     },
# }

# def send_msg(msg, receiver_number):

#     headers = {
#     'Authorization': 'Bearer EAAOp52EX6kgBO7GFrupNzaecHZBEswM0sJIptzZAYUdChYmW5ZBJlY5M1uEqUYlHqxTThwGRPY2z8bljv6rdztRVsgUnDU11G7YWdjfU4veOl2L1bMFW4hRvn4S01Vj0x0R7fT1j3fZBUXHuubbmqw1e37YGj1qKnicXExXY7Why74i5ZAbShip1xl1g9iTk6fpfKuQtGg1RgPypyN7Y29hvNQlG7ZC8VT6Hrrqcpsfljd4QzM',
#     }
    
#     # Check if the user's message contains any of the keywords
#     keywords = ["video", "image", "document"]
#     found_keyword = next((keyword for keyword in keywords if keyword in msg.lower()), None)
    
#     # Check for the presence of "details" or "information" in the message
#     if found_keyword:
#         keyword_data = keyword_to_data[found_keyword]
#         msg_type  = keyword_data["type"]
#         json_data = {
#             "messaging_product": "whatsapp",
#             "recipient_type": "individual",
#             "to": receiver_number,
#             "type": msg_type ,
#             msg_type : {
#                 "link": keyword_data["link"],
#                 "caption": keyword_data["caption"],
#             }
#         }
#     else:
#         json_data = {
#             "messaging_product": "whatsapp",
#             "recipient_type": "individual",
#             "to": receiver_number,
#             "type": "text",
#             "text": {
#                 "body": msg,
#             }
#         }

#     response = requests.post('https://graph.facebook.com/v17.0/132277916635812/messages', headers=headers, json=json_data)
#     print(response.text)

# @app.route('/receive_msg', methods=['POST', 'GET'])
# def webhook():
#     if request.method == 'GET':
#         # Handle the subscription verification request
#         hub_mode = request.args.get("hub.mode")
#         hub_challenge = request.args.get("hub.challenge")
#         if hub_mode == "subscribe" and hub_challenge:
#             hub_verify_token = request.args.get("hub.verify_token")
#             if hub_verify_token == VERIFY_TOKEN:
#                 return hub_challenge, 200
#             else:
#                 return "Verification token mismatch", 403
#     elif request.method == 'POST':
#         # Handle incoming WhatsApp messages
#         res = request.get_json()
#         print(res)
#         try:
#             if res['entry'][0]['changes'][0]['value']['messages'][0]['id']:
#                 chat_gpt_input = res['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
#                 completion = openai.ChatCompletion.create(
#                     model="gpt-3.5-turbo",
#                     messages=[{"role": "system", "content": system_message},
#                               {"role": "user", "content": chat_gpt_input}],
#                     max_tokens=100
#                 )
#                 response = completion['choices'][0]['message']['content']
#                 print("ChatGPT Response =>", response)
#                 receiver_number = res['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
#                 send_msg(response, receiver_number)
#         except Exception as e:
#             print("Error:", e)

#     return '200 OK HTTPS.'

# if __name__ == "__main__":
#     app.run(debug=True)


# ____________________________________________________________________


# from flask import Flask, request
# import requests
# import openai
# import os
# from system import system_message
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import json

# # Set up your OpenAI API key
# openai.api_key = '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'

# app = Flask(__name__)

# # Verification token for WhatsApp integration
# VERIFY_TOKEN = "farhan205"

# # Your custom function to send a notification via Outlook
# def send_notification_to_human(customer_request):
#     # Replace with your Outlook email configuration and recipient address
#     sender_email = "outlook_7FAF9B19D3F6568C@outlook.com"
#     sender_password = "S@m33r123"
#     recipient_email = "fafridi047@gmail.com"

#     subject = "Customer Request: Talk to a Human"
#     message = f"Customer wants to talk to a human. Request: {customer_request}"

#     try:
#         # Create a secure SMTP connection to the Outlook server
#         server = smtplib.SMTP("smtp.office365.com", 587)
#         server.starttls()

#         # Login to the sender's email account
#         server.login(sender_email, sender_password)

#         # Create a message
#         msg = MIMEMultipart()
#         msg["From"] = sender_email
#         msg["To"] = recipient_email
#         msg["Subject"] = subject

#         # Attach the message body
#         msg.attach(MIMEText(message, "plain"))

#         # Send the email
#         server.sendmail(sender_email, recipient_email, msg.as_string())

#         # Close the SMTP server
#         server.quit()

#         print("Notification email sent successfully.")
#     except Exception as e:
#         print("Error sending notification email:", str(e))

# def send_msg(msg, receiver_number):
#     headers = {
#         'Authorization': 'Bearer EAAOp52EX6kgBO7GFrupNzaecHZBEswM0sJIptzZAYUdChYmW5ZBJlY5M1uEqUYlHqxTThwGRPY2z8bljv6rdztRVsgUnDU11G7YWdjfU4veOl2L1bMFW4hRvn4S01Vj0x0R7fT1j3fZBUXHuubbmqw1e37YGj1qKnicXExXY7Why74i5ZAbShip1xl1g9iTk6fpfKuQtGg1RgPypyN7Y29hvNQlG7ZC8VT6Hrrqcpsfljd4QzM',
#     }
#     json_data = {
#         'messaging_product': 'whatsapp',
#         'to': receiver_number,
#         'type': 'text',
#         "text": {
#             "body": msg
#         }
#     }
#     response = requests.post('https://graph.facebook.com/v17.0/132277916635812/messages', headers=headers, json=json_data)
#     print(response.text)

# @app.route('/receive_msg', methods=['POST', 'GET'])
# def webhook():
#     if request.method == 'GET':
#         # Handle the subscription verification request
#         hub_mode = request.args.get("hub.mode")
#         hub_challenge = request.args.get("hub.challenge")
#         if hub_mode == "subscribe" and hub_challenge:
#             hub_verify_token = request.args.get("hub.verify_token")
#             if hub_verify_token == VERIFY_TOKEN:
#                 return hub_challenge, 200
#             else:
#                 return "Verification token mismatch", 403
#     elif request.method == 'POST':
#         # Handle incoming WhatsApp messages
#         res = request.get_json()
#         print(res)
#         try:
#             if res['entry'][0]['changes'][0]['value']['messages'][0]['id']:
#                 chat_gpt_input = res['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
#                 if "talk to a human" in chat_gpt_input.lower():
#                     # Customer wants to talk to a human
#                     send_notification_to_human(chat_gpt_input)
#                     response = "A human will be with you shortly."
#                 else:
#                     # Handle regular user queries with GPT-3.5 Turbo
#                     completion = openai.ChatCompletion.create(
#                         model="gpt-3.5-turbo",
#                         messages=[{"role": "system", "content": system_message},
#                                   {"role": "user", "content": chat_gpt_input}],
#                         max_tokens=50
#                     )
#                     response = completion['choices'][0]['message']['content']
#                 print("ChatGPT Response =>", response)
#                 receiver_number = res['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
#                 send_msg(response, receiver_number)
#         except Exception as e:
#             print("Error:", e)

#     return '200 OK HTTPS.'

# if __name__ == "__main__":
#     app.run(debug=True)
