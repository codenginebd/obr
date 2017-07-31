from book_rental.libs.downloader.downloader import Downloader
from engine.exceptions.br_exception import BRException
from generics.libs.writer.excel_file_writer import ExcelFileWriter
from generics.libs.writer.writter import Writter


class SalePriceDownloader(Downloader):

    def __init__(self, file_name, *args, **kwargs):
        super(SalePriceDownloader, self).__init__(file_name=file_name, *args, **kwargs)

    def get_default_writer(self):
        return ExcelFileWriter

    def get_header_names(self):
        return [
            "Product Code", "Is New", "Print Type", "Market Price", "Base Price", "Is Special Sale Offer", "Special Offer Rate", "Offer Start Date",
            "Offer End Date", "Currency Code"
        ]