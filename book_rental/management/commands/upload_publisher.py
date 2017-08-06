from django.core.management.base import BaseCommand

from book_rental.libs.uploader.author_uploader import AuthorUploader
from book_rental.libs.uploader.publisher_uploader import PublisherUploader
from book_rental.models.author import Author
from book_rental.models.book_publisher import BookPublisher
from generics.libs.reader.excel_file_reader import ExcelFileReader
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Upload Initialized")
        print("Now")
        BookPublisher.objects.all().delete()
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
        fname = PROJECT_ROOT + '/book_rental/management/commands/uploads/publisher_upload.xlsx'
        excel_reader = ExcelFileReader(file_name=fname, sheet_name='Sheet1')
        data = excel_reader.get_data()
        category_uploader = PublisherUploader(data=data)
        category_uploader.handle_upload()

        a_object = BookPublisher.objects.first()
        print(a_object.thumbnail.name)

        print("Upload done!")


