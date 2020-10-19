import django
from django.contrib import admin
from django.db.models import Count, F
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.db import models
import datetime
from app.models import TinTuc, NguonLuc, TinhNguyenVien, CuuHo, HoDan, Tinh, Huyen, Xa, Thon
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
    list_display = ('status', 'name', 'location', 'tinh', 'huyen', 'xa', 'thon', 'phone', 'volunteer')
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter), ('thon', RelatedDropdownFilter))
    search_fields = ('name', 'phone')

class CuuHoAdmin(admin.ModelAdmin):
    list_display = ('update_time', 'status', 'name', 'location', 'tinh', 'huyen', 'xa', 'thon', 'phone', 'volunteer')
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter), ('thon', RelatedDropdownFilter))
    search_fields = ('name', 'phone')

class TinhNguyenVienAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone')
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter), ('thon', RelatedDropdownFilter))
    search_fields = ('name', 'phone')
 
class HoDanAdmin(admin.ModelAdmin):
    list_display = ('update_time', 'status', 'name', 'need', 'get_note', 'location', 'tinh', 'huyen', 'xa', 'thon', 'phone', 'volunteer', 'cuuho')
    list_display_links = ('name', )
    list_editable = ('status', 'tinh', 'huyen', 'xa', 'thon', 'volunteer', 'cuuho')
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter), ('thon', RelatedDropdownFilter))
    search_fields = ('name', 'phone', 'note')

    def get_note(self, obj):
        if obj.note:
            return (' '.join(obj.note.split()[:10]) + '...')
        else:
            return ''
        
        get_note.short_description = 'Ghi chú'
    

admin.site.register(TinTuc, TinTucAdmin)
admin.site.register(NguonLuc, NguonLucAdmin)
admin.site.register(HoDan, HoDanAdmin)
admin.site.register(CuuHo, CuuHoAdmin)
admin.site.register(TinhNguyenVien, TinhNguyenVienAdmin)

admin.site.register(Tinh)
admin.site.register(Huyen)
admin.site.register(Xa)
admin.site.register(Thon)

