from django.core.management.base import BaseCommand
from openpyxl.workbook.workbook import Workbook
import os
from book_rental.libs.downloader.category_downloader import CategoryDownloader
from book_rental.libs.uploader.category_uploader import CategoryUploader
from generics.libs.reader.excel_file_reader import ExcelFileReader
from generics.libs.writer.excel_file_writer import ExcelFileWriter
from generics.libs.writer.writter import Writter


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Download Initialized")
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        fname = PROJECT_ROOT+ '/book_rental/management/commands/downloads/category_list1.xlsx'
        #print(issubclass(ExcelFileWriter, Writter))
        category_downloader = CategoryDownloader(file_name=fname, writer=ExcelFileWriter)
        category_downloader.download()



