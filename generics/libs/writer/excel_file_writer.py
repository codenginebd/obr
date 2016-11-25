from openpyxl.workbook.workbook import Workbook
from generics.libs.writer.writter import Writter


class ExcelFileWriter(Writter):
    def __init__(self, data, header=[], file_path=None, *args, **kwargs):
        super(ExcelFileWriter, self).__init__(data=data, header=header,
                                              file_path=file_path, *args, **kwargs)

    def write(self):
        self.workbook = Workbook()