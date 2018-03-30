import os
from django.conf import settings
from django.db import transaction
from datetime import datetime
from bauth.models.email import Email
from bauth.models.phone import Phone
from generics.libs.loader.loader import load_model
from generics.libs.utils import get_relative_path_to_media
from logger.models.error_log import ErrorLog


class AuthorUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        Author = load_model(app_label="book_rental", model_name="Author")
        self.data = self.data[1:]
        for row in self.data:
            try:
                with transaction.atomic():
                    index = 0
                    code = row[index].strip() if row[index] else None
                    index += 1
                    author_name = row[index] if row[index] else None
                    index += 1
                    author_name_2 = row[index] if row[index] else None
                    index += 1
                    author_description = row[index] if row[index] else None
                    index += 1
                    author_description_2 = row[index] if row[index] else None
                    index += 1
                    show_2 = row[index] if row[index] else None
                    index += 1
                    author_image = row[index] if row[index] else None
                    index += 1
                    date_of_birth = row[index] if row[index] else None
                    index += 1
                    emails = str(row[index]) if row[index] else None

                    if not author_name:
                        ErrorLog.log(url='', stacktrace='Author Name must be given', context='Author')
                        continue

                    if not author_description:
                        ErrorLog.log(url='', stacktrace='Author description must be given', context='Author')
                        continue

                    try:
                        if not show_2:
                            show_2 = 0
                        show_2 = int(show_2)
                        if show_2 == 1:
                            if not author_name_2 or not author_description_2:
                                ErrorLog.log(url='', stacktrace='Author name bn and author description bn missing. Data: %s skipping...' % row, context='Author')
                                continue
                    except Exception as exp:
                        ErrorLog.log(url='', stacktrace='Show 2 must be number. Given %s. skipping...' % show_2, context='Author')
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
                            ErrorLog.log(url='', stacktrace='Author with code %s not found. skipping...' % code, context='Author')
                            continue

                    if not author_object:
                        author_object = Author()

                    if author_name_2:
                        author_object.name_2 = author_name_2

                    if author_description_2:
                        author_object.description_2 = author_description_2

                    author_object.show_2 = show_2

                    if author_image:
                        image_full_path = os.path.join(settings.MEDIA_AUTHOR_PATH, author_image)
                        if os.path.exists(image_full_path):
                            image_name_relative_media = get_relative_path_to_media(image_full_path)
                            author_object.image.name = image_name_relative_media
                        else:
                            ErrorLog.log(url='', stacktrace='Author image %s not found. skipping...' % author_image, context='Author')
                            continue

                    if date_of_birth:
                        try:
                            date_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y")
                        except Exception as exp:
                            print(str(exp))
                            date_of_birth = None
                            ErrorLog.log(url='', stacktrace='Author date of birth format incorrect. Correct format: dd/mm/yyyy. skipping...', context='Author')
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
                            phone = phone.replace("'", "")
                            phone_objects = Phone.objects.filter(number=phone)
                            if phone_objects.exists():
                                phone_object = phone_objects.first()
                            else:
                                phone_object = Phone(number=phone)
                                phone_object.save()

                            if not author_object.phones.filter(pk=phone_object.pk).exists():
                                author_object.phones.add(phone_object)

            except Exception as exp:
                ErrorLog.log(url='', stacktrace='Exception Occured. Exception message: %s. Skipping...Date: %s' % (str(exp), row), context='Author')


        return True



