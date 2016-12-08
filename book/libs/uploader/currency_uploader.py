from django.db import transaction

from book.libs.uploader.uploader import Uploader
from book.models.currency import Currency
from brlogger.models.error_log import ErrorLog
from engine.exceptions.br_exception import BRException


class CurrencyUploader(Uploader):
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

            if len(row) != 2:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Invalid format in currency upload'
                error_log.save()
                continue
            currency_objects = Currency.objects.filter(short_name=row[0])
            if currency_objects.exists():
                currency_object = currency_objects.first()
            else:
                currency_object = Currency()
                currency_object.short_name = row[0]
            currency_object.name = row[1]
            currency_object.save()