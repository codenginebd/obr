
from engine.emailer.email_client import EmailClient
from rq.decorators import job


@job
def send_email_job(email_object):
    EmailClient.send_email(email_object["recipients"],email_object["subject"],email_object["html_body"],email_object["text_body"],from_email=None)