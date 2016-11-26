from django.db import transaction

from book.libs.uploader.uploader import Uploader
from book.models.language import Language
from brlogger.models.error_log import ErrorLog
from engine.exceptions.br_exception import BRException


class LanguageUploader(Uploader):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def data_as_list(self):
        if not self.data:
            raise BRException("No data found")

        data_list = []

        for currency_code, name in self.data.items():
            data_list += [[ currency_code.upper(), name ]]
        return data_list

    def handle_upload(self):

        self.data = self.data_as_list()

        for row in self.data:

            if len(row) != 3:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Invalid format in language upload'
                error_log.save()
                continue
            language_objects = Language.objects.filter(short_name=row[0])
            if language_objects.exists():
                language_object = language_objects.first()
            else:
                language_object = Language()
                language_object.short_name = row[0]
            language_object.name = row[1]
            language_object.save()