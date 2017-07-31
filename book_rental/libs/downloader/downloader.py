from generics.libs.writer.writter import Writter


class Downloader(object):
    def __init__(self, file_name, *args, **kwargs):
        self.file_name = file_name
        self.args = args
        self.kwargs = kwargs

    def get_default_writer(self):
        return Writter

    def get_header_names(self):
        return [

        ]

    def download(self, data=None, writer=None, *args, **kwargs):
        if data is None:
            return
            
        if not type(data) is list and not type(data) is tuple:
            return

        writer_class = writer if writer else self.get_default_writer()

        if issubclass(writer_class, Writter):
            writer_instance = writer_class(data=data,header=self.get_header_names(),
            file_path=self.file_name, *args, **kwargs)
            writer_instance.write()
        else:
            raise BRException("Writer must be an instance of Writter")

    def download_as_json(self, data=None, encoding='utf-8', writer=None, *args, **kwargs):
        pass