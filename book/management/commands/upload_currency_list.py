from django.core.management.base import BaseCommand
import os
from book.libs.uploader.currency_uploader import CurrencyUploader
from generics.libs.reader.json_file_reader import JSONFileReader


class Command(BaseCommand):

    def handle(self, *args, **options):
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        fname = PROJECT_ROOT + '/book/management/commands/uploads/currency_list.json'
        json_reader = JSONFileReader(file_name=fname)
        data = json_reader.get_data()
        currency_uploader = CurrencyUploader(data=data)
        currency_uploader.handle_upload()