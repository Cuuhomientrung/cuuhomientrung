import django
from django.contrib import admin
from django.db.models import Count, F
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
from dynamic_raw_id.admin import DynamicRawIDMixin
from dynamic_raw_id.filters import DynamicRawIDFilter
from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, \
    SliderNumericFilter
from mapbox_location_field.admin import MapAdmin
from mapbox_location_field.forms import LocationField
from django.forms import ModelForm
from simple_history.admin import SimpleHistoryAdmin

vi_formats.DATETIME_FORMAT = "d/m/y H:i"

PAGE_SIZE = 30

# admin interface

admin.site.site_header = 'Hệ thống thông tin Cứu hộ miền Trung'
admin.site.site_title = 'Hệ thống thông tin Cứu hộ miền Trung'
admin.index_title = 'Hệ thống thông tin Cứu hộ miền Trung'
admin.site_url = '/'


class PeopleNumericFilter(SliderNumericFilter):
    STEP = 1


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
    list_per_page = PAGE_SIZE

    def get_queryset(self, request):
        queryset = super(TinhNguyenVienAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related('tinh', 'huyen', 'xa')
        return queryset


class LocationForm(ModelForm):
    class Meta:
        model = HoDan
        fields = "__all__"
        exclude = ('tinh', 'huyen', 'thon',)

    geo_location = LocationField(
        required=False,
        map_attrs={
            "style": "mapbox://styles/mapbox/outdoors-v11",
            "zoom": 10,
            "center": [106.507467036133, 17.572843459110928],
            "cursor_style": 'pointer',
            "marker_color": "red",
            "rotate": False,
            "geocoder": True,
            "fullscreen_button": True,
            "navigation_buttons": True,
            "track_location_button": True,
            "readonly": True,
            "placeholder": "Chọn một địa điểm",
        }
    )


class HoDanHistoryAdmin(SimpleHistoryAdmin):
    history_list_display = [
        'history_date', 'history_type', 'status', 'get_note', 'volunteer',
        'cuuho', 'ip_address'
    ]


class HoDanAdmin(DynamicRawIDMixin, NumericFilterModelAdmin, MapAdmin, HoDanHistoryAdmin, admin.ModelAdmin):
    dynamic_raw_id_fields = ('tinh', 'huyen', 'xa', 'volunteer', 'cuuho')
    list_display = ('id', 'update_time', 'status', 'name', 'phone', 'get_note', 'people_number', 'location', 'tinh', 'huyen', 'xa', 'volunteer', 'cuuho')
    list_display_links = ('id', 'name', 'phone',)
    list_editable = ('status',)
    list_filter = (
        ('people_number', PeopleNumericFilter),
        ('status', ChoiceDropdownFilter),
        ('xa', DynamicRawIDFilter),
        'update_time',
    )
    search_fields = ('name', 'phone', 'note', 'id')
    actions = [export_ho_dan_as_excel_action()]
    form = LocationForm

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
