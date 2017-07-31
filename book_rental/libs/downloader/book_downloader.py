from book_rental.libs.downloader.downloader import Downloader
from engine.exceptions.br_exception import BRException
from generics.libs.writer.excel_file_writer import ExcelFileWriter
from generics.libs.writer.writter import Writter


class BookDownloader(Downloader):

    def __init__(self, file_name, *args, **kwargs):
        super(BookDownloader, self).__init__(file_name=file_name, *args, **kwargs)

    def get_default_writer(self):
        return ExcelFileWriter

    def get_header_names(self):
        return [
            "Code", "Book Title", "Book Subtitle", "ISBN", "Description", "Category Code(s)", "Edition",
            "Total Page", "Publisher Code", "Published date(dd/mm/YYYY)", "Cover Photo", "Language", "Keyword(s)"
        ]