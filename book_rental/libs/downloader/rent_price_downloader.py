from book_rental.libs.downloader.downloader import Downloader
from engine.exceptions.br_exception import BRException
from generics.libs.writer.excel_file_writer import ExcelFileWriter
from generics.libs.writer.writter import Writter


class RentPriceDownloader(Downloader):

    def __init__(self, file_name, *args, **kwargs):
        super(RentPriceDownloader, self).__init__(file_name=file_name, *args, **kwargs)

    def get_default_writer(self):
        return ExcelFileWriter

    def get_header_names(self):
        return [
            "Rent Plan Code", "Product Code", "Is New", "Print Type", "Price(%)", "Is Special Rent Offer", "Special Rent Rate",
            "Offer Start Date", "Offer End Date", "Currency Coode"
        ]