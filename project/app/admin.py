import datetime
import pytz
from django.contrib import admin
from django.db.models import Count, F, Count
from django.utils.safestring import mark_safe
from app.settings import TIME_ZONE
from app.models import TinTuc, TinhNguyenVien, CuuHo, HoDan, Tinh, Huyen, Xa,\
    TrangThaiHoDan
from app.views import BaseRestfulAdmin, HoDanRestFulModelAdmin
from app.utils.export_to_excel import export_ho_dan_as_excel_action, utc_to_local
from django.conf.locale.vi import formats as vi_formats
from django_admin_listfilter_dropdown.filters import (
    ChoiceDropdownFilter
)
from django_restful_admin import admin as rest_admin
from dynamic_raw_id.admin import DynamicRawIDMixin
from django.utils.html import format_html
from admin_numeric_filter.admin import NumericFilterModelAdmin, \
    SliderNumericFilter
from mapbox_location_field.admin import MapAdmin
from mapbox_location_field.forms import LocationField
from django.forms import ModelForm, ModelChoiceField
from simple_history.admin import SimpleHistoryAdmin
from app.settings import (
    REVISION
)
from admin_auto_filters.filters import AutocompleteFilter
from easy_select2.widgets import Select2

vi_formats.DATETIME_FORMAT = "d/m/y H:i"

PAGE_SIZE = 30

# admin interface

admin.site.site_header = 'Hệ thống thông tin Cứu hộ miền Trung'
admin.site.site_title = 'Hệ thống thông tin Cứu hộ miền Trung'
admin.index_title = 'Hệ thống thông tin Cứu hộ miền Trung'
admin.site_url = '/'


# Helper classes
class PeopleNumericFilter(SliderNumericFilter):
    STEP = 1


class StatusAdminFilter(AutocompleteFilter):
    title = 'Lọc theo trạng thái'
    field_name = 'status'


class TinhAdminFilter(AutocompleteFilter):
    title = 'Lọc theo tỉnh'
    field_name = 'tinh'


class HuyenAdminFilter(AutocompleteFilter):
    title = 'Lọc theo huyện'
    field_name = 'huyen'


class XaAdminFilter(AutocompleteFilter):
    title = 'Lọc theo xã'
    field_name = 'xa'


# Admin classes
class TinTucAdmin(admin.ModelAdmin):
    list_per_page = PAGE_SIZE
    list_display = ('update_time', 'title', 'url')
    search_fields = ('title',)


class NguonLucAdmin(admin.ModelAdmin):
    list_display = ('status', 'name', 'location', 'tinh',
                    'huyen', 'xa', 'phone', 'volunteer')
    list_filter = (
        ('status', ChoiceDropdownFilter),
        TinhAdminFilter,
        XaAdminFilter,
        HuyenAdminFilter,
    )
    search_fields = ('name', 'phone')
    list_editable = ('status',)
    list_per_page = PAGE_SIZE


class CuuHoLocationForm(ModelForm):
    class Meta:
        model = CuuHo
        fields = "__all__"
        exclude = ('thon',)
    
    def __init__(self, *args, **kwargs):
        super(CuuHoLocationForm, self).__init__(*args, **kwargs)
        self.fields["tinh"].queryset = Tinh.objects.order_by("name")
        self.fields['volunteer'] = ModelChoiceField(queryset=TinhNguyenVien.objects.all(), widget=Select2(), required=False)


class CuuHoAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    list_display = ('update_time', 'status', 'name', 'phone',
                    'location', 'tinh', 'huyen', 'xa', 'volunteer')
    list_filter = (
        ('status', ChoiceDropdownFilter),
        TinhAdminFilter,
        XaAdminFilter,
        HuyenAdminFilter,
    )
    search_fields = ('name', 'phone')
    list_editable = ('status',)
    list_per_page = PAGE_SIZE
    form = CuuHoLocationForm

    def get_queryset(self, request):
        queryset = super(CuuHoAdmin, self).get_queryset(request)
        queryset = queryset\
            .prefetch_related('tinh', 'huyen', 'xa', 'volunteer')\
            .order_by('-status')
        return queryset

    class Media:
        css = {
            'all': (f'/static/css/custom.css?v={REVISION}',)
        }


class TinhNguyenVienAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone', 'status')
    list_filter = (
        'status',
        TinhAdminFilter,
        XaAdminFilter,
        HuyenAdminFilter,
    )
    search_fields = ('name', 'phone')
    list_editable = ('status',)
    list_per_page = PAGE_SIZE

    def get_queryset(self, request):
        queryset = super(TinhNguyenVienAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related('tinh', 'huyen', 'xa')
        return queryset


class HoDanForm(ModelForm):
    class Meta:
        model = HoDan
        fields = "__all__"
        exclude = ('thon',)

    tinh = ModelChoiceField(queryset=Tinh.objects.all(), widget=Select2(), required=False)
    huyen = ModelChoiceField(queryset=Huyen.objects.all(), widget=Select2(), required=False)
    xa = ModelChoiceField(queryset=Xa.objects.all(), widget=Select2(), required=False)
    volunteer = ModelChoiceField(queryset=TinhNguyenVien.objects.all(), widget=Select2(), required=False)
    cuuho = ModelChoiceField(queryset=CuuHo.objects.all(), widget=Select2(), required=False)

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
    list_display = ('id', 'get_update_time', 'status', 'name', 'phone', 'get_note',
                    'people_number', 'location', 'tinh', 'huyen', 'xa', 'volunteer', 'cuuho')
    list_display_links = ('id', 'name', 'phone',)
    list_editable = ('status',)
    list_filter = (
        'status',
        TinhAdminFilter,
        XaAdminFilter,
        HuyenAdminFilter,
    )
    search_fields = ('name', 'phone', 'note', 'id')
    actions = [export_ho_dan_as_excel_action()]
    form = HoDanForm
    list_per_page = PAGE_SIZE

    def get_queryset(self, request):
        queryset = super(HoDanAdmin, self).get_queryset(request)
        queryset = queryset\
            .prefetch_related('tinh', 'huyen', 'xa', 'volunteer', 'cuuho', 'status')\
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
        compare_time = datetime.datetime(
            2020, 10, 22, 17, 0, 0, tzinfo=datetime.timezone.utc).astimezone(tz=pytz.timezone(TIME_ZONE))
        update_time = utc_to_local(obj.update_time).strftime("%m/%d/%Y %H:%M")
        if utc_to_local(obj.created_time) >= compare_time:
            return format_html('<div class="highlight-red"> {} </div>', update_time)
        else:
            return format_html('<div class="highlight-blue"> {} </div>', update_time)
    get_update_time.short_description = 'Cập nhật'
    get_update_time.allow_tags = True

    class Media:
        css = {
            'all': (f'/static/css/custom.css?v={REVISION}',)
        }


class HoDanCuuHoStatisticBase(admin.ModelAdmin):
    class Meta:
        abstract = True

    list_display = ('name', 'get_cuu_ho_san_sang', 'get_ho_dan_can_ung_cuu')
    search_fields = ('name', )
    list_per_page = PAGE_SIZE

    @mark_safe
    def get_cuu_ho_san_sang(self, obj):
        hodan = [item for item in obj.cuuho_reversed.all() if item.status == 1]
        tag = f'<a href="/app/cuuho/?{self.URL_CUSTOM_TAG}={obj.pk}&status=1">{len(hodan)}</a>'
        return tag
    get_cuu_ho_san_sang.short_description = "Đơn vị cứu hộ sẵn sàng"
    get_cuu_ho_san_sang.allow_tags = True

    @mark_safe
    def get_ho_dan_can_ung_cuu(self, obj):
        hodan = [item for item in obj.hodan_reversed.all() if item.status_id == 3]
        tag = f'<a href="/app/hodan/?{self.URL_CUSTOM_TAG}={obj.pk}&status_id=3">{len(hodan)}</a>'
        return tag
    get_ho_dan_can_ung_cuu.short_description = "Hộ dân cần ứng cứu"
    get_ho_dan_can_ung_cuu.allow_tags = True

    def get_queryset(self, request):
        queryset = super(HoDanCuuHoStatisticBase, self).get_queryset(request)
        queryset = queryset.prefetch_related(
            'cuuho_reversed', 'hodan_reversed')
        return queryset


class TinhAdmin(HoDanCuuHoStatisticBase):
    URL_CUSTOM_TAG = 'tinh'
    list_per_page = PAGE_SIZE


class HuyenAdmin(HoDanCuuHoStatisticBase):
    list_filter = (
        TinhAdminFilter,
    )
    URL_CUSTOM_TAG = 'huyen'
    list_per_page = PAGE_SIZE


class XaAdmin(HoDanCuuHoStatisticBase):
    list_filter = (
        'huyen__tinh',
        HuyenAdminFilter,
    )
    URL_CUSTOM_TAG = 'xa'

    def get_queryset(self, request):
        queryset = super(HoDanCuuHoStatisticBase,self).get_queryset(request)
        queryset = queryset.prefetch_related('cuuho_reversed', 'hodan_reversed')\
            .filter(hodan_reversed__status_id=3)\
            .annotate(total_hodan=Count("hodan_reversed"))\
            .order_by('-total_hodan')
        return queryset

    list_per_page=PAGE_SIZE


class ThonAdmin(HoDanCuuHoStatisticBase):
    list_filter = (
        TinhAdminFilter,
        HuyenAdminFilter,
    )
    URL_CUSTOM_TAG = 'thon'
    list_per_page = PAGE_SIZE


class TrangThaiHoDanAdmin(admin.ModelAdmin):

    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(TrangThaiHoDanAdmin, self).__init__(model, admin_site)


admin.site.register(TinTuc, TinTucAdmin)
# admin.site.register(NguonLuc, NguonLucAdmin)
admin.site.register(HoDan, HoDanAdmin)
admin.site.register(CuuHo, CuuHoAdmin)
admin.site.register(TinhNguyenVien, TinhNguyenVienAdmin)

admin.site.register(Tinh, TinhAdmin)
admin.site.register(Huyen, HuyenAdmin)
admin.site.register(Xa, XaAdmin)
admin.site.register(TrangThaiHoDan, TrangThaiHoDanAdmin)
# admin.site.register(Thon, ThonAdmin)

rest_admin.site.register(
    HoDan, view_class=HoDanRestFulModelAdmin, __doc__="hello")
rest_admin.site.register(CuuHo, view_class=BaseRestfulAdmin)
rest_admin.site.register(TinhNguyenVien, view_class=BaseRestfulAdmin)
rest_admin.site.register(Tinh, view_class=BaseRestfulAdmin)
rest_admin.site.register(Huyen, view_class=BaseRestfulAdmin)
rest_admin.site.register(Xa, view_class=BaseRestfulAdmin)
