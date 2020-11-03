import datetime
import pytz
from .settings import TIME_ZONE
from .admin import TinhAdmin
from .models import Tinh, HoDan, CuuHo, TinhNguyenVien
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse


def index(request):
    ho_dan_duoc_cuu_count = HoDan.objects.filter(status_id=7).count()
    ho_dan_can_cuu_count = HoDan.objects.filter(status_id=3).count()
    cuu_ho_count = CuuHo.objects.filter(status=1).count()

    # sort theo data tu 0:00 ngay 27 VNT
    # issue 155
    compare_time = datetime.datetime(2020, 10, 26, 17, 0, 0, tzinfo=datetime.timezone.utc).astimezone(tz=pytz.timezone(TIME_ZONE))

    ho_dan_new_group_by_tinh = Tinh.objects.prefetch_related('hodan_reversed')\
        .filter(hodan_reversed__created_time__gt=compare_time)\
        .annotate(total_hodan=Count("hodan_reversed"))\
        .order_by('-total_hodan')[0:5]

    ho_dan_can_cuu_group_by_tinh = Tinh.objects.prefetch_related('hodan_reversed')\
        .exclude(hodan_reversed__status_id=7)\
        .annotate(total_hodan=Count("hodan_reversed"))\
        .filter(id__in=[tinh.id for tinh in ho_dan_new_group_by_tinh])

    ho_dan_da_cuu_group_by_tinh = Tinh.objects.prefetch_related('hodan_reversed')\
        .filter(hodan_reversed__status_id=7)\
        .annotate(total_hodan=Count("hodan_reversed"))\
        .filter(id__in=[tinh.id for tinh in ho_dan_new_group_by_tinh])
    ho_dan_da_cuu_dict = dict((tinh.id, tinh.total_hodan) for tinh in ho_dan_da_cuu_group_by_tinh)

    cuu_ho_by_tinh = Tinh.objects.prefetch_related('cuuho_reversed')\
        .annotate(total_cuuho=Count("cuuho_reversed"))\
        .filter(id__in=[tinh.id for tinh in ho_dan_new_group_by_tinh])
    cuu_ho_dict = dict((tinh.id, tinh.total_cuuho) for tinh in cuu_ho_by_tinh)

    tinh_nguyen_vien_count = TinhNguyenVien.objects.count()

    hodan_url = reverse("admin:app_hodan_changelist")
    tinhInfos = [
        {
            "url": f'{hodan_url}?{TinhAdmin.URL_CUSTOM_TAG}={tinh.pk}',
            "total_hodan": tinh.total_hodan,
            "total_dacuu": ho_dan_da_cuu_dict.get(tinh.pk, 0),
            "total_cuuho": cuu_ho_dict.get(tinh.pk, 0),
            "id": tinh.pk,
            "name": tinh.name,
        } for tinh in ho_dan_can_cuu_group_by_tinh
    ]

    context = {
        'tong_hodan_cap_cuu': ho_dan_can_cuu_count,
        'tong_hodan_da_duoc_cuu': ho_dan_duoc_cuu_count,
        'tong_doi_cuu_ho': cuu_ho_count,
        'tong_tinh_nguyen_vien': tinh_nguyen_vien_count,
        'tinhInfos': tinhInfos,
    }
    return render(request, 'home_index.html', context=context)
