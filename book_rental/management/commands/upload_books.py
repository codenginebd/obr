from django.core.management.base import BaseCommand
import os
from book_rental.libs.uploader.book_uploader import BookUploader
from generics.libs.reader.excel_file_reader import ExcelFileReader


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Book Initializing...")
        print("Now")
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        fname = PROJECT_ROOT + '/book_rental/management/commands/uploads/book_list.xlsx'
        excel_reader = ExcelFileReader(file_name=fname, sheet_name='Sheet1')
        data = excel_reader.get_data()
        book_uploader = BookUploader(data=data)
        book_uploader.handle_upload()
        
        
        