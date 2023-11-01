import xlwt
import xlrd
from xlutils.copy import copy
import os

class Export:
    @classmethod
    def excel(cls, numberIds, names, dateList, timeList, fileName):
        book = xlwt.Workbook(encoding = 'utf-8')
        sheetAddRow = book.add_sheet('result attendance', cell_overwrite_ok = True)

        columnNumberId = 'Id'
        columnName = 'tên'
        columnDate = 'ngày'
        columnTime = 'giờ'
        n = 0
        sheetAddRow.write(0, 0, columnNumberId)
        sheetAddRow.write(0, 2, columnName)
        sheetAddRow.write(0, 4, columnDate)
        sheetAddRow.write(0, 6, columnTime)

        for m, e1 in enumerate(numberIds, n + 1):
            sheetAddRow.write(m, 0, e1)

        for m, e2 in enumerate(names, n + 1):
            sheetAddRow.write(m, 2, e2)

        for m, e3 in enumerate(dateList, n + 1):
            sheetAddRow.write(m, 4, e3)

        for m, e4 in enumerate(timeList, n + 1):
            sheetAddRow.write(m, 6, e4)

        return book.save(fileName)
    

def append_to_excel(checkid, checkname, checkdate, checktime, fileName):
    if not os.path.exists(fileName):
        # Tạo một tệp Excel mới nếu tệp chưa tồn tại
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sheet1')
        columnNumberId = 'Id'
        columnName = 'tên'
        columnDate = 'ngày'
        columnTime = 'giờ'
        
        # Ghi tiêu đề cho các cột
        worksheet.write(0, 0, columnNumberId)
        worksheet.write(0, 2, columnName)
        worksheet.write(0, 4, columnDate)
        worksheet.write(0, 6, columnTime)

        workbook.save(fileName)
        
    
    # Đọc dữ liệu từ tệp Excel đã tồn tại
    rb = xlrd.open_workbook(fileName)
    sheet = rb.sheet_by_index(0)
    rows = sheet.nrows

    # Tạo một bản sao có thể ghi vào tệp Excel đã tồn tại
    wb = copy(rb)
    sheet_write = wb.get_sheet(0)

    # Ghi dữ liệu mới vào các ô tương ứng
    for i in range(len(checkid)):
        sheet_write.write(rows + i, 0, checkid[i])
        sheet_write.write(rows + i, 2, checkname[i])
        sheet_write.write(rows + i, 4, checkdate[i])
        sheet_write.write(rows + i, 6, checktime[i])

    # Lưu bản sao với dữ liệu mới vào tệp Excel
    wb.save(fileName)
    

# # Sử dụng hàm append_to_excel để ghi tiếp dữ liệu vào tệp Excel
# append_to_excel(checkid, checkname, checkdate, checktime, fileName)

