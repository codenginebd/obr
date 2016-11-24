from django.core.management.base import BaseCommand
from book.libs.uploader.category_uploader import CurrencyUploader


class Command(BaseCommand):

    def handle(self, *args, **options):
        fname = '/home/codenginebd/Desktop/Projects/online-book-rental/book/management/commands/currency_list.json'
        json_reader = JSONFileReader(file_name=fname)
        data = json_reader.get_data()
        currency_uploader = CurrencyUploader(data=data)
        currency_uploader.handle_upload()