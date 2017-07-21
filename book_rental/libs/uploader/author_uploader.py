from django.db import transaction
# from brlogger.models.error_log import ErrorLog


class AuthorUploader(object):
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
                author_name = row[index] if row[index] else None
                index += 1
                author_description = row[index] if row[index] else None
                index += 1
                date_of_birth = row[index] if row[index] else None
                index += 1
                address = row[index] if row[index] else None
                index += 1
                emails = row[index] if row[index] else None
                index += 1
                phones = row[index] if row[index] else None
                index += 1
                number_of_books_published = row[index] if row[index] else None




