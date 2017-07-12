from django.core.management.base import BaseCommand
from book.libs.uploader.currency_lan_country_uploader import CountryLanCountryUploader
from generics.libs.reader.json_file_reader import JSONFileReader
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        fname = PROJECT_ROOT + '/book/management/commands/uploads/country_list.json'
        json_reader = JSONFileReader(file_name=fname)
        data = json_reader.get_data()
        country_uploader = CountryLanCountryUploader(data=data)
        country_uploader.handle_upload()