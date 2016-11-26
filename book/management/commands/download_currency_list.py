from django.core.management.base import BaseCommand

from book.libs.downloader.currency_downloader import CurrencyDownloader
from book.libs.uploader.currency_uploader import CurrencyUploader
from generics.libs.reader.json_file_reader import JSONFileReader


class Command(BaseCommand):

    def handle(self, *args, **options):
        fname = '/home/codenginebd/Desktop/Projects/online-book-rental/book/management/commands/downloads/currency_list.json'
        currency_downloader = CurrencyDownloader(file_name=fname)
        currency_downloader.download_as_json()