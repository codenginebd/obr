from django.core.management.base import BaseCommand
import os
from book_rental.libs.downloader.currency_downloader import CurrencyDownloader
from book_rental.libs.uploader.currency_uploader import CurrencyUploader
from generics.libs.reader.json_file_reader import JSONFileReader


class Command(BaseCommand):

    def handle(self, *args, **options):
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        fname = PROJECT_ROOT + '/book_rental/management/commands/downloads/currency_list.json'
        currency_downloader = CurrencyDownloader(file_name=fname)
        currency_downloader.download_as_json()