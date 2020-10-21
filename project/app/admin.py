import django
from django.contrib import admin
from django.db.models import Count, F, Count
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.db import models
import datetime
from app.models import TinTuc, NguonLuc, TinhNguyenVien, CuuHo, HoDan, Tinh, Huyen, Xa, Thon
from app.views import BaseRestfulAdmin, HoDanRestFulModelAdmin
from app.utils.export_to_excel import export_ho_dan_as_excel_action
from django.conf.locale.vi import formats as vi_formats
from django.forms import TextInput, Textarea
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django_restful_admin import admin as rest_admin
from rest_framework.permissions import AllowAny, IsAdminUser

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
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter))
    search_fields = ('name', 'phone')
    list_editable = ('status',)


class CuuHoAdmin(admin.ModelAdmin):
    list_display = ('update_time', 'status', 'name', 'phone', 'location', 'tinh', 'huyen', 'xa', 'volunteer')
    # list_editable = ('tinh', 'huyen', 'xa', 'volunteer')
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter), ('thon', RelatedDropdownFilter))
    search_fields = ('name', 'phone')
    list_editable = ('status',)


    def get_queryset(self, request):
        queryset = super(CuuHoAdmin, self).get_queryset(request)
        queryset = queryset\
            .prefetch_related('tinh', 'huyen', 'xa', 'volunteer')\
            .order_by('-status')
        return queryset



class TinhNguyenVienAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone', 'status')
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter))
    search_fields = ('name', 'phone')
    list_editable = ('status',)

    def get_queryset(self, request):
        queryset = super(TinhNguyenVienAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related('tinh', 'huyen', 'xa')
        return queryset


class HoDanAdmin(admin.ModelAdmin):
    list_display = ('update_time', 'status', 'name', 'phone', 'get_note', 'location', 'tinh', 'huyen', 'xa', 'volunteer', 'cuuho')
    list_display_links = ('name', 'phone')
    list_editable = ('status',)
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter))
    search_fields = ('name', 'phone', 'note')
    actions = [export_ho_dan_as_excel_action()]
    # Built-in auto complete selection from Django
    autocomplete_fields = ['volunteer', 'cuuho']

    def get_queryset(self, request):
        queryset = super(HoDanAdmin, self).get_queryset(request)
        queryset = queryset\
            .prefetch_related('tinh', 'huyen', 'xa', 'volunteer', 'cuuho')\
            .order_by('-status', '-update_time')

        return queryset

    def get_note(self, obj):
        if obj.note:
            return (' '.join(obj.note.split()[:80]) + '...')
        else:
            return ''
    get_note.short_description = 'Ghi chú'

    class Media:
        css = {
            'all': ('/static/css/custom.css',)
        }



class HoDanCuuHoStatisticBase(admin.ModelAdmin):
    class Meta:
        abstract = True

    list_display = ('name', 'get_cuu_ho_san_sang', 'get_ho_dan_can_ung_cuu')
    search_fields = ('name', )


    @mark_safe
    def get_cuu_ho_san_sang(self, obj):
        hodan = [item for item in obj.cuuho_reversed.all() if item.status == 1]
        tag = f'<a href="/app/cuuho/?{self.URL_CUSTOM_TAG}={obj.pk}&status=1">{len(hodan)}</a>'
        return tag
    get_cuu_ho_san_sang.short_description = "Đơn vị cứu hộ sẵn sàng"
    get_cuu_ho_san_sang.allow_tags = True

    @mark_safe
    def get_ho_dan_can_ung_cuu(self, obj):
        hodan = [item for item in obj.hodan_reversed.all() if item.status == 1]
        tag = f'<a href="/app/hodan/?{self.URL_CUSTOM_TAG}={obj.pk}&status=1">{len(hodan)}</a>'
        return tag
    get_ho_dan_can_ung_cuu.short_description = "Hộ dân cần ứng cứu"
    get_ho_dan_can_ung_cuu.allow_tags = True

    def get_queryset(self, request):
        queryset = super(HoDanCuuHoStatisticBase, self).get_queryset(request)
        queryset = queryset.prefetch_related('cuuho_reversed', 'hodan_reversed')

class TinhAdmin(HoDanCuuHoStatisticBase):
    URL_CUSTOM_TAG = 'tinh'



class HuyenAdmin(HoDanCuuHoStatisticBase):
    URL_CUSTOM_TAG = 'huyen'


class XaAdmin(HoDanCuuHoStatisticBase):
    URL_CUSTOM_TAG = 'xa'
    def get_queryset(self, request):
        queryset = super(HoDanCuuHoStatisticBase,self).get_queryset(request)
        queryset = queryset.prefetch_related('cuuho_reversed', 'hodan_reversed')\
        .filter(hodan_reversed__status=1).annotate(total_hodan=Count("hodan_reversed"))\
            .order_by('-total_hodan')
        return queryset



class ThonAdmin(HoDanCuuHoStatisticBase):
    URL_CUSTOM_TAG = 'thon'


admin.site.register(TinTuc, TinTucAdmin)
# admin.site.register(NguonLuc, NguonLucAdmin)
admin.site.register(HoDan, HoDanAdmin)
admin.site.register(CuuHo, CuuHoAdmin)
admin.site.register(TinhNguyenVien, TinhNguyenVienAdmin)

admin.site.register(Tinh, TinhAdmin)
admin.site.register(Huyen, HuyenAdmin)
admin.site.register(Xa, XaAdmin)
# admin.site.register(Thon, ThonAdmin)

rest_admin.site.register(HoDan, view_class=HoDanRestFulModelAdmin)
rest_admin.site.register(CuuHo, view_class=BaseRestfulAdmin)
rest_admin.site.register(TinhNguyenVien, view_class=BaseRestfulAdmin)
rest_admin.site.register(Tinh, view_class=BaseRestfulAdmin)
rest_admin.site.register(Huyen, view_class=BaseRestfulAdmin)
rest_admin.site.register(Xa, view_class=BaseRestfulAdmin)
