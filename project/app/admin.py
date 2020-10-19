import django
from django.contrib import admin
from django.db.models import Count, F
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.db import models
import datetime
from app.models import TinTuc, NguonLuc, TinhNguyenVien, CuuHo, HoDan, Tinh, Huyen, Xa, Thon
from app.utils.export_to_excel import export_ho_dan_as_excel_action
from django.conf.locale.vi import formats as vi_formats
from django.forms import TextInput, Textarea
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter

vi_formats.DATETIME_FORMAT = "d/m/y H:i"

# admin interface

admin.site.site_header = 'Hệ thống thông tin Cứu hộ miền Trung'
admin.site.site_title = 'Hệ thống thông tin Cứu hộ miền Trung'
admin.index_title = 'Hệ thống thông tin Cứu hộ miền Trung'
admin.site_url = '/'

class TinTucAdmin(admin.ModelAdmin):
    list_display = ('update_time', 'title', 'url')
    search_fields = ('title',)

class NguonLucAdmin(admin.ModelAdmin):
    list_display = ('status', 'name', 'location', 'tinh', 'huyen', 'xa', 'phone', 'volunteer')
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter), ('thon', RelatedDropdownFilter))
    search_fields = ('name', 'phone')

class CuuHoAdmin(admin.ModelAdmin):
    list_display = ('update_time', 'status', 'name', 'phone', 'location', 'tinh', 'huyen', 'xa', 'volunteer')
    list_editable = ('tinh', 'huyen', 'xa', 'volunteer')
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter), ('thon', RelatedDropdownFilter))
    search_fields = ('name', 'phone')

class TinhNguyenVienAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone')
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter), ('thon', RelatedDropdownFilter))
    search_fields = ('name', 'phone')


class HoDanAdmin(admin.ModelAdmin):
    list_display = ('update_time', 'status', 'name', 'phone', 'get_note', 'location', 'tinh', 'huyen', 'xa', 'volunteer', 'cuuho')
    list_display_links = ('name', 'phone')
    list_editable = ('status', 'tinh', 'huyen', 'xa', 'volunteer', 'cuuho')
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter), ('thon', RelatedDropdownFilter))
    search_fields = ('name', 'phone', 'note')
    actions = [export_ho_dan_as_excel_action()]

    def get_note(self, obj):
        if obj.note:
            return (' '.join(obj.note.split()[:15]) + '...')
        else:
            return ''
    get_note.short_description = 'Ghi chú'

    export_ho_dan_as_excel_action.short_description = "Xuất file excel"

class TinhAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_cuu_ho_san_sang', 'get_ho_dan_can_ung_cuu')

    @mark_safe
    def get_cuu_ho_san_sang(self, obj):
        count = CuuHo.objects.filter(tinh=obj, status=1).count()
        tag = f'<a href="/app/cuuho/?tinh={obj.pk}&status=1">{count}</a>'
        return tag

    get_cuu_ho_san_sang.short_description = "Đơn vị cứu hộ sẵn sàng"
    get_cuu_ho_san_sang.allow_tags = True

    @mark_safe
    def get_ho_dan_can_ung_cuu(self, obj):
        count = HoDan.objects.filter(tinh=obj).exclude(status=3).count()
        tag = f'<a href="/app/hodan/?tinh={obj.pk}">{count}</a>'
        return str(count)
    get_cuu_ho_san_sang.short_description = "Đơn vị cứu hộ sẵn sàng"

class HuyenAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_cuu_ho_san_sang', 'get_ho_dan_can_ung_cuu')

    def get_cuu_ho_san_sang(self, obj):
        count = CuuHo.objects.filter(huyen=obj, status=1).count()
        return str(count)
    get_cuu_ho_san_sang.short_description = "Đơn vị cứu hộ sẵn sàng"

    def get_ho_dan_can_ung_cuu(self, obj):
        count = HoDan.objects.filter(huyen=obj).exclude(status=3).count()
        return str(count)
    get_ho_dan_can_ung_cuu.short_description = "Hộ dân cần ứng cứu"

class XaAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_cuu_ho_san_sang', 'get_ho_dan_can_ung_cuu')

    def get_cuu_ho_san_sang(self, obj):
        count = CuuHo.objects.filter(xa=obj, status=1).count()
        return str(count)
    get_cuu_ho_san_sang.short_description = "Đơn vị cứu hộ sẵn sàng"

    def get_ho_dan_can_ung_cuu(self, obj):
        count = HoDan.objects.filter(xa=obj).exclude(status=3).count()
        return str(count)
    get_ho_dan_can_ung_cuu.short_description = "Hộ dân cần ứng cứu"

class ThonAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_cuu_ho_san_sang', 'get_ho_dan_can_ung_cuu')

    def get_cuu_ho_san_sang(self, obj):
        count = CuuHo.objects.filter(thon=obj, status=1).count()
        return str(count)
    get_cuu_ho_san_sang.short_description = "Đơn vị cứu hộ sẵn sàng"

    def get_ho_dan_can_ung_cuu(self, obj):
        count = HoDan.objects.filter(thon=obj).exclude(status=3).count()
        return str(count)
    get_ho_dan_can_ung_cuu.short_description = "Hộ dân cần ứng cứu"

admin.site.register(TinTuc, TinTucAdmin)
# admin.site.register(NguonLuc, NguonLucAdmin)
admin.site.register(HoDan, HoDanAdmin)
admin.site.register(CuuHo, CuuHoAdmin)
admin.site.register(TinhNguyenVien, TinhNguyenVienAdmin)

admin.site.register(Tinh, TinhAdmin)
admin.site.register(Huyen, HuyenAdmin)
admin.site.register(Xa, XaAdmin)
# admin.site.register(Thon, ThonAdmin)
