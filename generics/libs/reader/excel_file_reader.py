# Dependancy on openpyxl
import openpyxl

from engine.exceptions.br_exception import BRException
from generics.libs.reader.file_reader import FileReader


class ExcelFileReader(FileReader):

    def __init__(self, file_name=None, *args, **kwargs):
        super(ExcelFileReader, self).__init__(file_name=file_name, *args, **kwargs)

    def read_file(self):
        self.workbook = openpyxl.load_workbook(self.file_name)
        self.sheet_name = self.kwargs.get('sheet_name')
        all_sheets = self.workbook.get_sheet_names()
        if all_sheets:
            if self.sheet_name:
                if self.sheet_name in all_sheets:
                    pass
                else:
                    self.sheet_name = all_sheets[0]
            else:
                self.sheet_name = all_sheets[0]
        else:
            raise BRException("No sheets found")

        self.sheet = self.workbook.get_sheet_by_name(self.sheet_name)

        self.start_row = self.kwargs.get('start_row') if self.kwargs.get('start_row') else 2
        self.start_column = self.kwargs.get('start_col') if self.kwargs.get('start_col') else 2
        contents = []
        for row in self.sheet.iter_rows():
            row_list = []
            for cell in row:
                row_list += [ cell.value ]
            contents += [ row_list ]
        return contents


