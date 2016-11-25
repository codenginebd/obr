from django.core.management.base import BaseCommand
from openpyxl.workbook.workbook import Workbook

from book.libs.uploader.category_uploader import CategoryUploader
from generics.libs.reader.excel_file_reader import ExcelFileReader


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Download Initialized")
        fname = '/home/codenginebd/Desktop/Projects/online-book-rental/book/management/commands/category_list1.xlsx'
        wb = Workbook()
        sheet = wb.create_sheet(title='Sheet Title')
        sheet.cell(row=1,column=2, value='Hello')
        wb.save(fname)



