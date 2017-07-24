from django.db import transaction
from datetime import datetime
from bauth.models.email import Email
from bauth.models.phone import Phone
from book_rental.models.author import Author


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

                if not author_object:
                    author_object = Author()

                if date_of_birth:
                    try:
                        date_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y")
                    except Exception as exp:
                        date_of_birth = None

                    if date_of_birth:
                        author_object.date_of_birth = date_of_birth

                author_object.name = author_name
                author_object.description = author_description
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






