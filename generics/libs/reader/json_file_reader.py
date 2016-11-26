import json

from generics.libs.reader.file_reader import FileReader


class JSONFileReader(FileReader):

    def __init__(self, file_name=None, *args, **kwargs):
        super(JSONFileReader, self).__init__(file_name=file_name, *args, **kwargs)

    def read_file(self):
        file_contents = None
        with open(self.file_name, 'r') as f:
            file_contents = f.read()
        json_data = json.loads(file_contents, encoding='utf-8')
        return json_data
