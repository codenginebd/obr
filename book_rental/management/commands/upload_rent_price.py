from django.core.management.base import BaseCommand
from book_rental.libs.uploader.price_matrix_uploader import PriceMatrixUploader
from generics.libs.reader.excel_file_reader import ExcelFileReader
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Upload Initialized")
        print("Now")
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        fname = PROJECT_ROOT + '/book_rental/management/commands/uploads/rent_price.xlsx'
        excel_reader = ExcelFileReader(file_name=fname, sheet_name='Sheet1')
        data = excel_reader.get_data()
        category_uploader = PriceMatrixUploader(data=data,price_type='rent')
        category_uploader.handle_upload()

        print("Upload done!")