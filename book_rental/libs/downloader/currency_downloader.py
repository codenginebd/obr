from book_rental.libs.downloader.downloader import Downloader
from engine.exceptions.br_exception import BRException
from generics.libs.writer.json_file_writer import JSONFileWriter
from generics.libs.writer.writter import Writter
from generics.models.sales.currency import Currency


class CurrencyDownloader(Downloader):

    def __init__(self, file_name, *args, **kwargs):
        super(CurrencyDownloader, self).__init__(file_name=file_name, *args, **kwargs)

    def get_default_writer(self):
        return JSONFileWriter

    def download_as_json(self, queryset=None, encoding='utf-8', writer=None, *args, **kwargs):

        data_rows = []
        if not queryset:
            queryset = Currency.objects.all()

        data_rows = queryset.values_list('short_name', 'name')

        data_object = {}
        for data_row in data_rows:
            data_object[data_row[0]] = data_row[1]

        writer_class = writer if writer else self.get_default_writer()

        if issubclass(writer_class, Writter):
            writer_instance = writer_class(data=data_object, file_path=self.file_name, *args, **kwargs)
            writer_instance.write()



