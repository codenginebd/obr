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

    def download(self, queryset=None, writer=None, *args, **kwargs):
        pass

    def download_as_json(self, queryset=None, encoding='utf-8', writer=None, *args, **kwargs):
        pass