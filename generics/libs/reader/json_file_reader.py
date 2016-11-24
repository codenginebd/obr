import json

class JSONFileReader(FileReader):

    def __init__(self, file_name=None, *args, **kwargs):
        super(JSONFileReader, self).__init__(file_name=file_name, *args, **kwargs)

    def read_file(self):
        json_data = json.loads(self.file_name)
        return json_data