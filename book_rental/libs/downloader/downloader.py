from engine.exceptions.br_exception import BRException
from generics.libs.writer.writter import Writter


class Downloader(object):
    def __init__(self, file_name, *args, **kwargs):
        self.file_name = file_name
        self.args = args
        self.kwargs = kwargs

    def get_default_writer(self):
        return Writter

    def download(self, data=None, writer=None, *args, **kwargs):
        if data is None:
            return
            
        if not type(data) is list and not type(data) is tuple:
            return

        headers = kwargs.get("headers", [])

        writer_class = writer if writer else self.get_default_writer()

        if issubclass(writer_class, Writter):
            writer_instance = writer_class(data=data,header=headers,
            file_path=self.file_name, *args, **kwargs)
            writer_instance.write()
            return self.file_name
        else:
            raise BRException("Writer must be an instance of Writter")

    def download_as_json(self, data=None, encoding='utf-8', writer=None, *args, **kwargs):
        pass