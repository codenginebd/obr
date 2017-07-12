from django.core.management.base import BaseCommand
from openpyxl.workbook.workbook import Workbook
import os
from book.libs.downloader.category_downloader import CategoryDownloader
from book.libs.uploader.category_uploader import CategoryUploader
from generics.libs.reader.excel_file_reader import ExcelFileReader
from generics.libs.writer.excel_file_writer import ExcelFileWriter
from generics.libs.writer.writter import Writter


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Download Initialized")
        PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
        fname = PROJECT_ROOT+ 'book/management/commands/downloads/category_list1.xlsx'
        #print(issubclass(ExcelFileWriter, Writter))
        category_downloader = CategoryDownloader(file_name=fname, writer=ExcelFileWriter)
        category_downloader.download()



