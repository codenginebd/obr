from django.db import transaction
# from brlogger.models.error_log import ErrorLog
from book_rental.models.book_publisher import BookPublisher


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
                publisher_description = row[index] if row[index] else None
                index += 1
                publisher_image = row[index] if row[index] else None
                index += 1
                emails = row[index] if row[index] else None
                index += 1
                phones = row[index] if row[index] else None
                
                if code:
                    publisher_objects = BookPublisher.objects.filter(code=code)
                    if publlisher_objects.exists():
                       publisher_object = publisher_objects.first()
                    else:
                        raise Exception("Publisher with code %s not exist in the system." % code)
                else:
                    publisher_object = BookPublisher()
                    
                if not publisher_name:
                    pass #Log error message
                    
                if not publisher_description:
                    pass #Log error
                
                publisher_object.name = publisher_name
                publisher_object.description  = publisher_description
                
                
                if publisher_image:
                    image_full_path = os.path.join(settings.MEDIA_PUBLISHER_PATH, publisher_image)
                    if os.path.exists(image_full_path):
                        image_file = File(open(image_full_path))
                        publisher_object.image = image_file
                
                
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
                
                
                    
                    
                
                    
                    

