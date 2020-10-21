import django
from django.contrib import admin
from django.db.models import Count, F
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.db import models
import datetime
import pytz
from app.models import TinTuc, NguonLuc, TinhNguyenVien, CuuHo, HoDan, Tinh, Huyen, Xa, Thon
from app.views import BaseRestfulAdmin, HoDanRestFulModelAdmin
from app.utils.export_to_excel import export_ho_dan_as_excel_action, utc_to_local
from django.conf.locale.vi import formats as vi_formats
from django.forms import TextInput, Textarea
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django_restful_admin import admin as rest_admin
from rest_framework.permissions import AllowAny, IsAdminUser
from dynamic_raw_id.admin import DynamicRawIDMixin
from dynamic_raw_id.filters import DynamicRawIDFilter
from django.utils.html import format_html

vi_formats.DATETIME_FORMAT = "d/m/y H:i"

PAGE_SIZE = 30

# admin interface

admin.site.site_header = 'Hệ thống thông tin Cứu hộ miền Trung'
admin.site.site_title = 'Hệ thống thông tin Cứu hộ miền Trung'
admin.index_title = 'Hệ thống thông tin Cứu hộ miền Trung'
admin.site_url = '/'


class TinTucAdmin(admin.ModelAdmin):
    list_per_page=PAGE_SIZE
    list_display = ('update_time', 'title', 'url')
    search_fields = ('title',)


class NguonLucAdmin(admin.ModelAdmin):
    list_display = ('status', 'name', 'location', 'tinh', 'huyen', 'xa', 'phone', 'volunteer')
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter))
    search_fields = ('name', 'phone')
    list_editable = ('status',)
    list_per_page=PAGE_SIZE

class CuuHoAdmin(admin.ModelAdmin):
    list_display = ('update_time', 'status', 'name', 'phone', 'location', 'tinh', 'huyen', 'xa', 'volunteer')
    # list_editable = ('tinh', 'huyen', 'xa', 'volunteer')
    list_filter = (('status', ChoiceDropdownFilter), ('tinh', RelatedDropdownFilter),('huyen', RelatedDropdownFilter), ('xa', RelatedDropdownFilter), ('thon', RelatedDropdownFilter))
    search_fields = ('name', 'phone')
    list_editable = ('status',)
    list_per_page=PAGE_SIZE

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
    list_per_page=PAGE_SIZE
    def get_queryset(self, request):
        queryset = super(TinhNguyenVienAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related('tinh', 'huyen', 'xa')
        return queryset


class HoDanAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ('tinh', 'huyen', 'xa', 'volunteer', 'cuuho')
    list_display = ('id', 'get_update_time', 'status', 'name', 'phone', 'get_note', 'location', 'tinh', 'huyen', 'xa', 'volunteer', 'cuuho')
    list_display_links = ('id', 'name', 'phone',)
    list_editable = ('status',)
    list_filter = (
        'id',
        ('status', ChoiceDropdownFilter),
        ('xa', DynamicRawIDFilter),
    )
    search_fields = ('name', 'phone', 'note', 'id')
    actions = [export_ho_dan_as_excel_action()]
    exclude = ('tinh', 'huyen', 'thon',)


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

    def get_update_time(self, obj):
        # TODO: ho tro trong vong 3 ngay
        # se remove code ngay sau do
        # 23 / 10 / 2020 00:00:00 GMT + 7
        compare_time = datetime.datetime(2020, 10, 22, 17, 0, 0, tzinfo=datetime.timezone.utc).astimezone(tz=pytz.timezone("Asia/Ho_Chi_Minh"))
        update_time = utc_to_local(obj.update_time).strftime("%m/%d/%Y %H:%M")
        if utc_to_local(obj.created_time) >= compare_time:
            return format_html('<div class="highlight-red"> {} </div>', update_time)
        else:
            return format_html('<div class="highlight-blue"> {} </div>', update_time)
    get_update_time.short_description = 'Cập nhật'
    get_update_time.allow_tags = True

    class Media:
        css = {
            'all': ('/static/css/custom.css',)
        }


class HoDanCuuHoStatisticBase(admin.ModelAdmin):
    class Meta:
        abstract = True

    list_display = ('name', 'get_cuu_ho_san_sang', 'get_ho_dan_can_ung_cuu')
    search_fields = ('name', )
    list_per_page=PAGE_SIZE
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
        return queryset



class TinhAdmin(HoDanCuuHoStatisticBase):
    URL_CUSTOM_TAG = 'tinh'
    list_per_page=PAGE_SIZE



class HuyenAdmin(HoDanCuuHoStatisticBase):
    search_fields = ('name',)
    list_filter = (
        ('tinh', ChoiceDropdownFilter),
    )
    URL_CUSTOM_TAG = 'huyen'
    list_per_page=PAGE_SIZE


class XaAdmin(HoDanCuuHoStatisticBase):
    search_fields = ('name',)
    list_filter = (
        ('huyen', ChoiceDropdownFilter),
    )
    URL_CUSTOM_TAG = 'xa'
    list_per_page=PAGE_SIZE



class ThonAdmin(HoDanCuuHoStatisticBase):
    search_fields = ('name',)
    list_filter = (
        ('huyen', ChoiceDropdownFilter),
    )
    URL_CUSTOM_TAG = 'thon'
    list_per_page=PAGE_SIZE


admin.site.register(TinTuc, TinTucAdmin)
# admin.site.register(NguonLuc, NguonLucAdmin)
admin.site.register(HoDan, HoDanAdmin)
admin.site.register(CuuHo, CuuHoAdmin)
admin.site.register(TinhNguyenVien, TinhNguyenVienAdmin)

admin.site.register(Tinh, TinhAdmin)
admin.site.register(Huyen, HuyenAdmin)
admin.site.register(Xa, XaAdmin)
# admin.site.register(Thon, ThonAdmin)

rest_admin.site.register(HoDan, view_class=HoDanRestFulModelAdmin,__doc__="hello")
rest_admin.site.register(CuuHo, view_class=BaseRestfulAdmin)
rest_admin.site.register(TinhNguyenVien, view_class=BaseRestfulAdmin)
rest_admin.site.register(Tinh, view_class=BaseRestfulAdmin)
rest_admin.site.register(Huyen, view_class=BaseRestfulAdmin)
rest_admin.site.register(Xa, view_class=BaseRestfulAdmin)
