from book.libs.downloader.downloader import Downloader
from book.models.category import BookCategory
from engine.exceptions.br_exception import BRException
from generics.libs.writer.excel_file_writer import ExcelFileWriter
from generics.libs.writer.writter import Writter


class CategoryDownloader(Downloader):

    def __init__(self, file_name, *args, **kwargs):
        super(CategoryDownloader, self).__init__(file_name=file_name, *args, **kwargs)

    def get_default_writer(self):
        return ExcelFileWriter

    def get_header_names(self):
        return [
            "Code", "Category Name", "Parent"
        ]

    def download(self, queryset=None, writer=None, *args, **kwargs):
        if queryset is None:
            queryset = BookCategory.objects.all()

        contents = queryset.values_list('code', 'name', 'parent__name')

        writer_class = writer if writer else self.get_default_writer()

        if issubclass(writer_class, Writter):
            writer_instance = writer_class(data=contents,header=self.get_header_names(),
            file_path=self.file_name, *args, **kwargs)
            writer_instance.write()
        else:
            raise BRException("Writer must be an instance of Writter")



