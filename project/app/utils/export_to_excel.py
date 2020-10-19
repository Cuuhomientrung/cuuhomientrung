# import csv
import io
import xlsxwriter
from django.http import HttpResponse

def write_a_row(worksheet, row, array):
    col = 0
    for x in array:
        worksheet.write(row, col, x)
        col += 1

def export_as_excel_action(fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_excel(modeladmin, request, queryset):
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])

        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset

        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        file_name = modeladmin.model._meta.model.__name__

        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        row = 0
        if header:
            write_a_row(worksheet, row, field_names)
            row += 1
        for obj in queryset:
            write_a_row(worksheet, row, [str(getattr(obj, field)) for field in field_names])
            row += 1

        workbook.close()

        output.seek(0)

        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f"attachment; filename={file_name}.xlsx"

        output.close()

        return response

    return export_as_excel
