from django.core.management.base import BaseCommand
from book_rental.libs.uploader.category_uploader import CategoryUploader
from generics.libs.reader.excel_file_reader import ExcelFileReader


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Upload Initialized")
        print("Now")
        fname = '/home/codenginebd/Desktop/Projects/online-book_rental-rental/generics/management/commands/uploads/geo_list.xlsx'
        excel_reader = ExcelFileReader(file_name=fname, sheet_name='Sheet1')
        data = excel_reader.get_data()
        print(data)
        # category_uploader = CategoryUploader(data=data)
        # category_uploader.handle_upload()
        print("Upload done!")


