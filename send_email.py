import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
import datetime

from dotenv import load_dotenv  # pip install python-dotenv

PORT = 587  
EMAIL_SERVER = "smtp.gmail.com"  # Adjust server address, if you are not using @outlook

# Load the environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Read environment variables
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")


def send_email(subject, receiver_email, name):
    # Create the base text message.
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Chatbot", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
        {datetime.datetime.now().strftime('%d-%B-%Y (%I:%M %p)')}

        Dear {name}, How are you?
        """
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())


if __name__ == "__main__":
    send_email(
        subject="Chatbot",
        name="Farhan",
        receiver_email="fafridi047@gmail.com",
    )