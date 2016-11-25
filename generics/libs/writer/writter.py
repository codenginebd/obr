from generics.libs.reader.mixins.file_write_mixin import FileWriteMixin


class Writter(FileWriteMixin):
    def __init__(self, data, header=[], file_path=None, *args, **kwargs):
        self.file_name = None
        self.args = None
        self.kwargs = None
        self.data = data

    def write(self):
        pass
