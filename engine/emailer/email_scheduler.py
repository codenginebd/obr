from django.conf import settings

from brlogger.models.email_log import EmailLog
from engine.emailer.jobs import send_email_job

__author__ = 'Sohel'


class EmailScheduler(object):
    def __init__(self):
        pass

    @classmethod
    def skeleton(cls):
        return  """recipients:[e1,e2,e3],
                subject: Registration Confirmation,
                html_body: <html><head></head><body><p style="color: black;">Please click on the <a href="'+ servers.APP_SERVER_HOST+":"+ str(servers.APP_SERVER_PORT) +'/email_verification/?token=%s">link</a> to complete the registration process.</p><div>Thank you!</div></body></html>' % (user_obj.activation_code,),
                text_body: Text Body"""

    @classmethod
    def place_to_queue(cls,email_object):
        # result = send_email_job.delay(email_object)

        from_email = email_object.get('from_email')
        if not from_email:
            from_email = settings.EMAIL_HOST_USER

        result = send_email_job.delay(email_object)

        for receipient in email_object['recipients']:
            email_log = EmailLog()
            email_log.sender = from_email
            email_log.receiver = receipient
            email_log.subject = email_object['subject']
            email_log.html_body = email_object['html_body']
            email_log.text_body = email_object['text_body']
            email_log.job_id = result.id
            email_log.status = "SUCCESSFUL"
            email_log.save()