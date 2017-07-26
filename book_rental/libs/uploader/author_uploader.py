import os
from django.conf import settings
from django.db import transaction
from datetime import datetime
from bauth.models.email import Email
from bauth.models.phone import Phone
from book_rental.models.author import Author
from generics.libs.utils import get_relative_path_to_media
from logger.models.error_log import ErrorLog


class AuthorUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        self.data = self.data[1:]
        for row in self.data:
            with transaction.atomic():
                index = 0
                code = row[index].strip() if row[index] else None
                index += 1
                author_name = row[index] if row[index] else None
                index += 1
                author_description = row[index] if row[index] else None
                index += 1
                author_image = row[index] if row[index] else None
                index += 1
                date_of_birth = row[index] if row[index] else None
                index += 1
                emails = str(row[index]) if row[index] else None

                if not author_name:
                    error_log = ErrorLog()
                    error_log.url = ''
                    error_log.stacktrace = 'Author name must be given'
                    error_log.save()
                    continue

                if not author_description:
                    error_log = ErrorLog()
                    error_log.url = ''
                    error_log.stacktrace = 'Author description must be given'
                    error_log.save()
                    continue

                if emails:
                    emails = emails.split(',')
                else:
                    emails = []

                index += 1
                phones = str(row[index]) if row[index] else None
                if phones:
                    phones = phones.split(',')
                else:
                    phones = []
                index += 1

                author_object = None

                if code:
                    author_objects = Author.objects.filter(code=code)
                    if author_objects.exists():
                        author_object = author_objects.first()
                    else:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Author with code %s not found. skipping...' % code
                        error_log.save()
                        continue

                if not author_object:
                    author_object = Author()

                if author_image:
                    image_full_path = os.path.join(settings.MEDIA_AUTHOR_PATH, author_image)
                    if os.path.exists(image_full_path):
                        image_name_relative_media = get_relative_path_to_media(image_full_path)
                        author_object.image.name = image_name_relative_media
                    else:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Author image %s not found. skipping...' % author_image
                        error_log.save()
                        continue

                if date_of_birth:
                    try:
                        date_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y")
                    except Exception as exp:
                        date_of_birth = None
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Author date of birth format incorrect. Correct format: dd/mm/yyyy. skipping...'
                        error_log.save()
                        continue

                    if date_of_birth:
                        author_object.date_of_birth = date_of_birth

                author_object.name = str(author_name)
                author_object.description = str(author_description)
                author_object.save()

                author_object.emails.clear()

                if emails:
                    for email in emails:
                        email_objects = Email.objects.filter(email=email)
                        if email_objects.exists():
                            email_object = email_objects.first()
                        else:
                            email_object = Email(email=email)
                            email_object.save()

                        if not author_object.emails.filter(pk=email_object.pk).exists():
                            author_object.emails.add(email_object)

                author_object.phones.clear()

                if phones:
                    for phone in phones:
                        phone_objects = Phone.objects.filter(number=phone)
                        if phone_objects.exists():
                            phone_object = phone_objects.first()
                        else:
                            phone_object = Phone(number=phone)
                            phone_object.save()

                        if not author_object.phones.filter(pk=phone_object.pk).exists():
                            author_object.phones.add(phone_object)






