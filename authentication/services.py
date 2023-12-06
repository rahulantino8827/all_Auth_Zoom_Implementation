import os
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class Util:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email="hitachipmei@gmail.com",
            to=[data["to_email"]],
        )
        email.send()

image_open = open(r"C:\Users\Antino\Desktop\abcdhjk.jpg", 'rb').read()
image_ready = MIMEImage(image_open,'.jpg',name="abcdhjk")
def send_email(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email="hitachipmei@gmail.com",
            to=[data["to_email"]],
        )
        email.attach(image_ready)

    
        email.send()