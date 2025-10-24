
from flask_mail import Mail, Message
mail = Mail()

def send_email(subject:str,recipients:list,html_body:str):
    msg = Message(subject,recipients=recipients,html=html_body)
    mail.send(msg)