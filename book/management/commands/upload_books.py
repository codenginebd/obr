from django.core.management.base import BaseCommand

from book.libs.uploader.book_uploader import BookUploader
from generics.libs.reader.excel_file_reader import ExcelFileReader


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Book Initializing...")
        print("Now")
        fname = '/home/codenginebd/Desktop/Projects/online-book-rental/book/management/commands/book_list.xlsx'
        excel_reader = ExcelFileReader(file_name=fname, sheet_name='Sheet1')
        data = excel_reader.get_data()
        book_uploader = BookUploader(data=data)
        book_uploader.handle_upload()
        
        
        