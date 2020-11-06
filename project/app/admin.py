import datetime
import pytz
from django.contrib import admin
from django.utils.safestring import mark_safe
from django_select2.forms import ModelSelect2Widget
from rest_framework import routers

from app.settings import TIME_ZONE
from app.models import TinTuc, TinhNguyenVien, CuuHo, HoDan, Tinh, Huyen, Xa,\
    TrangThaiHoDan, CUUHO_STATUS, TINHNGUYEN_STATUS
from app.views import CuuHoViewSet, HoDanViewSet,\
    TinhNguyenVienViewSet, TinhViewSet, HuyenViewSet, XaViewSet, TrangThaiHoDanSet
from app.utils.export_to_excel import export_ho_dan_as_excel_action, utc_to_local
from app.utils.safe_url import make_url_clickable, sanitize_url
from django.conf.locale.vi import formats as vi_formats
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter, RelatedDropdownFilter
from django.utils.html import format_html
from admin_numeric_filter.admin import NumericFilterModelAdmin, \
    SliderNumericFilter
from mapbox_location_field.admin import MapAdmin
from mapbox_location_field.forms import LocationField
from django.forms import ModelForm, ModelChoiceField, Textarea, TextInput
from django.db.models import Count, Q
from simple_history.admin import SimpleHistoryAdmin
from app.settings import (
    REVISION
)
from admin_auto_filters.filters import AutocompleteFilter
from django.urls import reverse
from easy_select2.widgets import Select2
from .utils.phone_number import PHONE_REGEX

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

class TinTucAdminForm(ModelForm):
    def clean_url(self):
        # do something that validates your data
        return sanitize_url(self.cleaned_data["url"])

class TinTucAdmin(admin.ModelAdmin):
    list_per_page = PAGE_SIZE
    list_display = ('update_time', 'title', 'show_url')
    search_fields = ('title',)
    form = TinTucAdminForm

    def show_url(self, obj):
        return make_url_clickable(obj.url)

class NguonLucAdmin(admin.ModelAdmin):
    list_display = ('status', 'name', 'location', 'tinh',
                    'huyen', 'xa', 'phone', 'volunteer')
    list_filter = (
        ('status', ChoiceDropdownFilter),
        TinhAdminFilter,
        HuyenAdminFilter,
        XaAdminFilter,
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

        self.fields['volunteer'] = ModelChoiceField(queryset=TinhNguyenVien.objects.order_by("-status"),
                                               widget=ModelSelect2Widget(
                                                   model=TinhNguyenVien,
                                                   search_fields=['name__unaccent__icontains'],
                                                   attrs={'style': 'min-width:250px', 'data-minimum-input-length': 0}
                                               ), required=False)

        self.fields["tinh"] = ModelChoiceField(queryset=Tinh.objects.order_by("name"),
                                               widget=ModelSelect2Widget(
                                                   model=Tinh,
                                                   search_fields=['name__unaccent__icontains'],
                                                   attrs={'style': 'min-width:250px', 'data-minimum-input-length': 0}
                                               ), required=False)

        self.fields["huyen"] = ModelChoiceField(queryset=Huyen.objects.order_by("name"),
                                                widget=ModelSelect2Widget(
                                                    model=Huyen,
                                                    search_fields=['name__unaccent__icontains'],
                                                    dependent_fields={'tinh': 'tinh'},
                                                    attrs={'style': 'min-width:250px', 'data-minimum-input-length': 0}
                                                ), required=False)

        self.fields["xa"] = ModelChoiceField(queryset=Xa.objects.order_by("name"),
                                             widget=ModelSelect2Widget(
                                                 model=Xa,
                                                 search_fields=['name__unaccent__icontains'],
                                                 dependent_fields={'huyen': 'huyen'},
                                                 attrs={'style': 'min-width:250px', 'data-minimum-input-length': 0}
                                             ), required=False)

        self.fields["tinh"].label = "Tỉnh"
        self.fields["tinh"].help_text = "Nhấn vào để chọn tỉnh"

        self.fields["huyen"].label = "Huyện"
        self.fields["huyen"].help_text = "Bạn phải chọn tỉnh trước"

        self.fields["xa"].label = "Xã"
        self.fields["xa"].help_text = "Bạn phải chọn tỉnh, và huyện trước"


class CuuHoAdmin(admin.ModelAdmin):
    list_display = ('update_time', 'status', 'name', 'phone',
                    'location', 'tinh', 'huyen', 'xa', 'volunteer')
    list_filter = (
        ('status', ChoiceDropdownFilter),
        TinhAdminFilter,
        HuyenAdminFilter,
        XaAdminFilter,
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
        ('status', ChoiceDropdownFilter),
        TinhAdminFilter,
        HuyenAdminFilter,
        XaAdminFilter,
    )
    search_fields = ('name', 'phone')
    list_editable = ('status',)
    list_per_page = PAGE_SIZE

    def get_queryset(self, request):
        queryset = super(TinhNguyenVienAdmin, self).get_queryset(request)
        queryset = queryset\
            .prefetch_related('tinh', 'huyen', 'xa')\
            .order_by('-status')
        return queryset


# Helper function
def _display_choices(choices, value):
    for choice in choices:
        if choice[0] == value:
            return choice[1]
    return ''


class HoDanForm(ModelForm):
    class Meta:
        model = HoDan
        fields = "__all__"
        exclude = ('thon',),
        labels = {
            "name": "Tiêu đề",
            "phone": "Số điện thoại",
        }
        widgets = {
            'note': Textarea(
                attrs={'placeholder': 'Ví dụ:\n17:00 23/10: Có người lớn bị cảm cúm.\n20:39 23/10: Đã gọi xác minh bệnh.\n'}
            ),
            'name': TextInput(attrs={'size': 50}),
            'phone': TextInput(attrs={'size': 50})
        }

    def __init__(self, *args, **kwargs):
        super(HoDanForm, self).__init__(*args, **kwargs)
        self.fields["tinh"] = ModelChoiceField(queryset=Tinh.objects.order_by("name"),
                                               widget=ModelSelect2Widget(
                                                   model=Tinh,
                                                   search_fields=['name__unaccent__icontains'],
                                                   attrs={'style': 'min-width:250px', 'data-minimum-input-length': 0}
                                               ), required=False)

        self.fields["huyen"] = ModelChoiceField(queryset=Huyen.objects.order_by("name"),
                                                widget=ModelSelect2Widget(
                                                    model=Huyen,
                                                    search_fields=['name__unaccent__icontains'],
                                                    dependent_fields={'tinh': 'tinh'},
                                                    attrs={'style': 'min-width:250px', 'data-minimum-input-length': 0}
                                                ), required=False)

        self.fields["xa"] = ModelChoiceField(queryset=Xa.objects.order_by("name"),
                                             widget=ModelSelect2Widget(
                                                 model=Xa,
                                                 search_fields=['name__unaccent__icontains'],
                                                 dependent_fields={'huyen': 'huyen'},
                                                 attrs={'style': 'min-width:250px', 'data-minimum-input-length': 0}
                                             ), required=False)

        self.fields['volunteer'] = ModelChoiceField(queryset=TinhNguyenVien.objects.all(), widget=Select2(), required=False)
        self.fields['cuuho'] = ModelChoiceField(queryset=CuuHo.objects.all(), widget=Select2(), required=False)

        self.fields['volunteer'].label_from_instance = self.label_from_volunteer
        self.fields['volunteer'].label = 'Tình nguyện viên'

        self.fields['cuuho'].label_from_instance = self.label_from_cuuho
        self.fields['cuuho'].label = 'Đội cứu hộ'

        self.fields["tinh"].label = "Tỉnh"
        self.fields["tinh"].help_text = "Nhấn vào để chọn tỉnh"

        self.fields["huyen"].label = "Huyện"
        self.fields["huyen"].help_text = "Bạn phải chọn tỉnh trước"

        self.fields["xa"].label = "Xã"
        self.fields["xa"].help_text = "Bạn phải chọn tỉnh, và huyện trước"

        self.fields['geo_location'] = LocationField(
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
                "placeholder": "Chọn một địa điểm trên bản đồ",
            }
        )

    @staticmethod
    def label_from_volunteer(obj):
        status = _display_choices(TINHNGUYEN_STATUS, obj.status)
        return f"{obj.name} | {obj.phone} | {status}"

    @staticmethod
    def label_from_cuuho(obj):
        status = _display_choices(CUUHO_STATUS, obj.status)
        return f"{obj.name} | {obj.phone} | {status}"

    volunteer = ModelChoiceField(
        queryset=TinhNguyenVien.objects.all(), widget=Select2(), required=False,
        help_text="Tên | Số điện thoại | Trạng thái"
    )
    cuuho = ModelChoiceField(
        queryset=CuuHo.objects.all(), widget=Select2(), required=False,
        help_text="Tên | Số điện thoại | Trạng thái"
    )

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


class HoDanAdmin(NumericFilterModelAdmin, MapAdmin, HoDanHistoryAdmin, admin.ModelAdmin):
    list_display = (
        'id', 'created_time', 'status', 'name', 'phone', 'get_note',
        'people_number', 'location', 'tinh', 'huyen', 'xa', 'volunteer', 'cuuho',
        'get_update_time'
    )
    fieldsets = (
        (None, {
           'fields': ('name', 'phone', 'status')
        }),
        ('Thông tin', {
            'fields': ('note', 'people_number', 'volunteer', 'cuuho',),
        }),
        ('Địa điểm', {
            'fields': ('location', 'tinh', 'huyen', 'xa', 'geo_location'),
        }),
    )
    list_display_links = ('id', 'name', 'phone',)
    list_editable = ()
    list_filter = (
        ('status', RelatedDropdownFilter),
        TinhAdminFilter,
        HuyenAdminFilter,
        XaAdminFilter,
    )
    search_fields = ('name', 'phone', 'note', 'id')
    actions = [export_ho_dan_as_excel_action()]
    form = HoDanForm
    list_per_page = PAGE_SIZE
    add_form_template = 'admin/app/hodan/change_form.html'
    change_form_template = 'admin/app/hodan/change_form.html'

    def pre_check_phone(self, request, form_url='', extra_context=None):
        from django.http import JsonResponse
        from .views import HoDanSerializer

        # Build query string
        phone_numbers = request.GET.get('phone_numbers', '').split(',')
        current_object_id = request.GET.get('object_id', None)
        regex = '^.*(%s).*$' % '|'.join(phone_numbers)
        filter_query = {'phone_expored__iregex': regex}
        queryset = HoDan.objects.filter(**filter_query)
        if current_object_id:
            queryset = queryset.exclude(pk=current_object_id)

        hodans = HoDanSerializer(queryset, many=True)
        for item in hodans.data:
            item.update({
                'view_url': reverse('admin:app_hodan_change', kwargs={
                    'object_id': item.get('id')
                }),
            })

        # Return json data (based on api serializers)
        return JsonResponse({
            "success": True,
            "items": hodans.data,
            "similar_hodan": list()
        })

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        # Append more context
        context.update({
            'PHONE_REGEX': PHONE_REGEX
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_urls(self):
        from django.urls import path
        from functools import update_wrapper

        urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        return [
            # pre_check_phone url
            path(
                'pre_check_phone/',
                wrap(self.pre_check_phone),
                name='%s_%s_pre_check_phone' % info
            ),
            # Origin urls
            *urls,
        ]

    def get_queryset(self, request):
        queryset = super(HoDanAdmin, self).get_queryset(request)
        queryset = queryset\
            .prefetch_related('tinh', 'huyen', 'xa', 'volunteer', 'cuuho', 'status')\
            .order_by('-created_time')

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
        #compare_time = datetime.datetime(
        #    2020, 10, 22, 17, 0, 0, tzinfo=datetime.timezone.utc).astimezone(tz=pytz.timezone(TIME_ZONE))
        compare_time = int(datetime.datetime.now().strftime("%Y%m%d"))-3
        update_time = utc_to_local(obj.update_time).strftime("%m/%d/%Y %H:%M")
        created_time = int(utc_to_local(obj.created_time).strftime("%Y%m%d"))
        if created_time >= compare_time:
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
    search_fields = ('name__unaccent', )
    list_per_page = PAGE_SIZE

    @mark_safe
    def get_cuu_ho_san_sang(self, obj):
        cuuho = [item for item in obj.cuuho_reversed.all() if item.status == 1]
        url = reverse('admin:app_cuuho_changelist')
        tag = f'<a href="{url}?{self.URL_CUSTOM_TAG}={obj.pk}&status=1">{len(cuuho)}</a>'
        return tag
    get_cuu_ho_san_sang.short_description = "Đơn vị cứu hộ sẵn sàng"
    get_cuu_ho_san_sang.allow_tags = True

    @mark_safe
    def get_ho_dan_can_ung_cuu(self, obj):
        hodan = [item for item in obj.hodan_reversed.all() if item.status_id == 3]
        url = reverse('admin:app_hodan_changelist')
        tag = f'<a href="{url}?{self.URL_CUSTOM_TAG}={obj.pk}&status_id=3">{len(hodan)}</a>'
        return tag
    get_ho_dan_can_ung_cuu.short_description = "Hộ dân cần ứng cứu"
    get_ho_dan_can_ung_cuu.allow_tags = True

    def get_queryset(self, request):
        queryset = super(HoDanCuuHoStatisticBase,self).get_queryset(request)
        queryset = queryset.prefetch_related('cuuho_reversed', 'hodan_reversed')\
            .annotate(total_hodan=Count("hodan_reversed", filter=Q(hodan_reversed__status_id=3)))\
            .order_by('-total_hodan')
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
        ('huyen__tinh', RelatedDropdownFilter),
        HuyenAdminFilter,
    )
    URL_CUSTOM_TAG = 'xa'
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


router = routers.DefaultRouter()
router.register('cuuho', CuuHoViewSet)
router.register('hodan', HoDanViewSet)
router.register('tinhnguyenvien', TinhNguyenVienViewSet)
router.register('tinh', TinhViewSet)
router.register('huyen', HuyenViewSet)
router.register('xa', XaViewSet)
router.register('hodan_status', TrangThaiHoDanSet)
