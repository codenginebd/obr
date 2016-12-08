from django.db import transaction

from book.libs.uploader.uploader import Uploader
from book.models.language import Language
from logger.models.error_log import ErrorLog
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

        for entry in self.data:
            data_list += [[ entry['alpha2'], entry['English'] ]]
        return data_list

    def handle_upload(self):

        Language.objects.all().delete()

        self.data = self.data_as_list()

        for row in self.data:

            if len(row) != 2:
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
