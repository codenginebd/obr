from django.core.management.base import BaseCommand
from book.libs.uploader.category_uploader import LanguageUploader


class Command(BaseCommand):

    def handle(self, *args, **options):
        fname = '/home/codenginebd/Desktop/Projects/online-book-rental/book/management/commands/language_list.json'
        json_reader = JSONFileReader(file_name=fname)
        data = json_reader.get_data()
        language_uploader = LanguageUploader(data=data)
        language_uploader.handle_upload()