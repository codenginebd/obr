from generics.libs.reader.mixins.file_read_mixin import FileReadMixin


class Reader(FileReadMixin):
    def __init__(self, file_name=None, *args, **kwargs):
        self.file_name = None
        self.args = None
        self.kwargs = None
        self.load_data(file_name=file_name, *args, **kwargs)

    def load_data(self, file_name=None, *args, **kwargs):
        self.file_name = file_name
        self.args = args
        self.kwargs = kwargs
        self.data = self.read_file(file_name=file_name)
