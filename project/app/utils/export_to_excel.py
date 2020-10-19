# import csv
import io
import xlsxwriter
from django.http import HttpResponse
from app.models import CUUHO_STATUS

def write_a_row(worksheet, row, array):
    col = 0
    for x in array:
        worksheet.write(row, col, x)
        col += 1

def lookup_in_a_list_of_tuples(arr, key):
    for x in arr:
        if x[0] == key:
            return x[1]

def export_ho_dan_as_excel_action(fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_excel(modeladmin, request, queryset):
        opts = modeladmin.model._meta
        field_names = ["name", "status", "location", "tinh", "xa", "huyen", "phone", "cuuho", "update_time", "note"]
        display_names = ["Tên hộ dân", "Tình trạng", "Vị trí", "Tỉnh", "Xã", "Huyện", "Sdt", "Cứu hộ", "Thời gian cuối cùng cập nhật", "Ghi chú"]
        file_name = "Danh_sach_ho_dan"

        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        row = 0
        if header:
            write_a_row(worksheet, row, display_names)
            row += 1
        for obj in queryset:
            arr = []
            for field in field_names:
                if field == "status":
                    arr.append(lookup_in_a_list_of_tuples(CUUHO_STATUS, getattr(obj, field)))
                else:
                    arr.append(str(getattr(obj, field) or ""))
            write_a_row(worksheet, row, arr)
            row += 1

        workbook.close()

        output.seek(0)

        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f"attachment; filename={file_name}.xlsx"

        output.close()

        return response

    return export_as_excel
