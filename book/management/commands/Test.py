import openpyxl
wb= openpyxl.load_workbook('book_list.xlsx')
sheet_names = wb.get_sheet_names()
sheet=wb.get_sheet_by_name('Sheet1')
print(sheet.cell(row=2,column=2).value)