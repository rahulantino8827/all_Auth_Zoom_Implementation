from django.core.mail import EmailMessage

def send_mail(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email="hitachipmei@gmail.com",
            to=[data["to_email"]],
        )
        email.send()