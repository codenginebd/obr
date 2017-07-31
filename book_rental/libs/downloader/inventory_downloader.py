from book_rental.libs.downloader.downloader import Downloader
from engine.exceptions.br_exception import BRException
from generics.libs.writer.excel_file_writer import ExcelFileWriter
from generics.libs.writer.writter import Writter


class InventoryDownloader(Downloader):

    def __init__(self, file_name, *args, **kwargs):
        super(InventoryDownloader, self).__init__(file_name=file_name, *args, **kwargs)

    def get_default_writer(self):
        return ExcelFileWriter

    def get_header_names(self):
        return [
            "Code", "Warehouse Code", "Book Code", "Item Total", "Is New?", "Available For Rent", "Print Type", "Supplier Name",
            "Address 1", "Address2", "Address3", "Address4", "Phone1", "Phone2", "Note"
        ]