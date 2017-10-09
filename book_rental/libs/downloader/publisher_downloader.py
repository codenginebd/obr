from book_rental.libs.downloader.downloader import Downloader
from generics.libs.writer.excel_file_writer import ExcelFileWriter


class PublisherDownloader(Downloader):

    def __init__(self, file_name=None, *args, **kwargs):
        super(PublisherDownloader, self).__init__(file_name=file_name, *args, **kwargs)

    def get_default_writer(self):
        return ExcelFileWriter