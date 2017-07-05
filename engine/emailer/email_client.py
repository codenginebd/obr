from django.conf import settings
from django.core.mail import EmailMultiAlternatives


__author__ = 'Codengine'


class EmailClient:
    def __init__(self):
        print("Inside Email Sender Class.")

    @classmethod
    def send_email(cls,email_to,email_sub,html_body,text_body,from_email=None):
        try:
            if not from_email:
                from_email = settings.EMAIL_HOST_USER
            email = EmailMultiAlternatives(subject=email_sub, body=text_body, from_email=from_email,
                                               to=email_to)
            email.attach_alternative(html_body, "text/html")
            return email.send(fail_silently=True)
        except Exception as msg:
            pass