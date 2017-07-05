import json
from engine.exceptions.br_exception import BRException
from generics.libs.writer.writter import Writter


class JSONFileWriter(Writter):
    def __init__(self, data, header=[], file_path=None, *args, **kwargs):
        super(JSONFileWriter, self).__init__(data=data, header=header,
                                              file_path=file_path, *args, **kwargs)

    def write(self):
        with open(self.file_name, 'w') as f:
            f.write(json.dumps(self.data, indent=4, sort_keys=True))