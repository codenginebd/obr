from django.conf import settings
from django.db import transaction
import os
from bauth.models.email import Email
from bauth.models.phone import Phone
from book_rental.models.book_publisher import BookPublisher
from generics.libs.utils import get_relative_path_to_media
from logger.models.error_log import ErrorLog


class PublisherUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        for row in self.data:
            with transaction.atomic():
                index = 0
                code = row[index].strip() if row[index] else None
                index += 1
                publisher_name = row[index] if row[index] else None
                index += 1
                publisher_name_2 = row[index] if row[index] else None
                index += 1
                publisher_description = row[index] if row[index] else None
                index += 1
                publisher_description_2 = row[index] if row[index] else None
                index += 1
                show_2 = row[index] if row[index] else None
                index += 1
                publisher_image = row[index] if row[index] else None
                index += 1
                emails = row[index] if row[index] else None
                index += 1
                phones = row[index] if row[index] else None

                if not publisher_name:
                    error_log = ErrorLog()
                    error_log.url = ''
                    error_log.stacktrace = 'Publisher name must be given'
                    error_log.save()
                    continue

                if not publisher_description:
                    error_log = ErrorLog()
                    error_log.url = ''
                    error_log.stacktrace = 'Publisher description must be given'
                    error_log.save()
                    continue

                try:
                    if not show_2:
                        show_2 = 0
                    show_2 = int(show_2)
                    if show_2 == 1:
                        if not publisher_name_2 or not publisher_description_2:
                            error_log = ErrorLog()
                            error_log.url = ''
                            error_log.stacktrace = 'Publisher name bn and Publisher description bn missing. Data: %s skipping...' % row
                            error_log.save()
                            continue
                except Exception as exp:
                    error_log = ErrorLog()
                    error_log.url = ''
                    error_log.stacktrace = 'Show BN must be number. Given %s. skipping...' % show_2
                    error_log.save()
                    continue
                
                if code:
                    publisher_objects = BookPublisher.objects.filter(code=code)
                    if publisher_objects.exists():
                       publisher_object = publisher_objects.first()
                    else:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Publisher with code %s not found. skipping...' % code
                        error_log.save()
                        continue
                else:
                    publisher_object = BookPublisher()
                
                publisher_object.name = str(publisher_name)
                publisher_object.description  = str(publisher_description)

                if publisher_name_2:
                    publisher_object.name_2 = publisher_name_2

                if publisher_description_2:
                    publisher_object.description_2 = publisher_description_2

                publisher_object.show_2 = show_2

                if publisher_image:
                    image_full_path = os.path.join(settings.MEDIA_PUBLISHER_PATH, publisher_image)
                    if os.path.exists(image_full_path):
                        image_name_relative_media = get_relative_path_to_media(image_full_path)
                        publisher_object.image.name = image_name_relative_media
                    else:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Publisher image %s not found. skipping...' % publisher_image
                        error_log.save()
                        continue

                publisher_object.save()
                
                publisher_object.emails.clear()
                
                if emails:
                    for email in emails:
                        email_objects = Email.objects.filter(email=email)
                        if email_objects.exists():
                            email_object = email_objects.first()
                        else:
                            email_object = Email(email=email)
                            email_object.save()

                        if not publisher_object.emails.filter(pk=email_object.pk).exists():
                            publisher_object.emails.add(email_object)

                publisher_object.phones.clear()

                if phones:
                    for phone in phones:
                        phone_objects = Phone.objects.filter(number=phone)
                        if phone_objects.exists():
                            phone_object = phone_objects.first()
                        else:
                            phone_object = Phone(number=phone)
                            phone_object.save()

                        if not publisher_object.phones.filter(pk=phone_object.pk).exists():
                            publisher_object.phones.add(phone_object)
                
                
                    
                    
                
                    
                    

