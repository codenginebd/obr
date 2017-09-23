from generics.libs.reader.mixins.file_write_mixin import FileWriteMixin


class Writter(FileWriteMixin):
    def __init__(self, data, header=[], file_path=None, *args, **kwargs):
        self.file_name = file_path
        self.args = args
        self.kwargs = kwargs
        self.header = header
        self.data = data
        self.response = kwargs.get("response", None)

    def write(self):
        pass
