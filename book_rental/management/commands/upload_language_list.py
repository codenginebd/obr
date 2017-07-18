from django.core.management.base import BaseCommand
import os
from book_rental.libs.uploader.language_uploader import LanguageUploader
from generics.libs.reader.json_file_reader import JSONFileReader


class Command(BaseCommand):

    def handle(self, *args, **options):
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        fname = PROJECT_ROOT + '/book_rental/management/commands/uploads/language_list.json'
        json_reader = JSONFileReader(file_name=fname)
        data = json_reader.get_data()
        language_uploader = LanguageUploader(data=data)
        language_uploader.handle_upload()