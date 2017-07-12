from django.core.management.base import BaseCommand
from book.libs.uploader.category_uploader import CategoryUploader
from generics.libs.reader.excel_file_reader import ExcelFileReader
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Upload Initialized")
        print("Now")
        PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
        fname = PROJECT_ROOT + 'book/management/commands/uploads/category_list1.xlsx'
        excel_reader = ExcelFileReader(file_name=fname, sheet_name='Sheet1')
        data = excel_reader.get_data()
        category_uploader = CategoryUploader(data=data)
        category_uploader.handle_upload()
        print("Upload done!")
        
        
        