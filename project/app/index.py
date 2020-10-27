from app.admin import TinhAdmin
from app.models import Tinh, HoDan, CuuHo, TinhNguyenVien
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse


def index(request):
    ho_dan_count = HoDan.objects.count()
    ho_dan_duoc_cuu_count = HoDan.objects.filter(status_id=7).count()
    ho_dan_can_cuu_count = ho_dan_count - ho_dan_duoc_cuu_count

    cuu_ho_count = CuuHo.objects.count()

    ho_dan_can_cuu_group_by_tinh = Tinh.objects.prefetch_related('hodan_reversed')\
        .exclude(hodan_reversed__status_id=7)\
        .annotate(total_hodan=Count("hodan_reversed"))\
        .order_by('-total_hodan')[0:5]

    ho_dan_da_cuu_group_by_tinh = Tinh.objects.prefetch_related('hodan_reversed')\
        .filter(hodan_reversed__status_id=7)\
        .annotate(total_hodan=Count("hodan_reversed"))\
        .filter(id__in=[tinh.id for tinh in ho_dan_can_cuu_group_by_tinh])
    ho_dan_da_cuu_dict = dict((tinh.id, tinh.total_hodan) for tinh in ho_dan_da_cuu_group_by_tinh)

    cuu_ho_by_tinh = Tinh.objects.prefetch_related('cuuho_reversed')\
        .annotate(total_cuuho=Count("cuuho_reversed"))\
        .filter(id__in=[tinh.id for tinh in ho_dan_can_cuu_group_by_tinh])
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
        } for tinh in  ho_dan_can_cuu_group_by_tinh
    ]

    context = {
        'tong_hodan_cap_cuu': ho_dan_can_cuu_count,
        'tong_hodan_da_duoc_cuu': ho_dan_duoc_cuu_count,
        'tong_doi_cuu_ho': cuu_ho_count,
        'tong_tinh_nguyen_vien': tinh_nguyen_vien_count,
        'tinhInfos': tinhInfos,


        'hodan_url' : reverse("admin:app_hodan_changelist"),
        'them_hodan_url': reverse("admin:app_hodan_add"),
        'them_cuuho_url': reverse("admin:app_cuuho_add"),
        'cuuho_url': reverse("admin:app_cuuho_changelist"),
        'tinhnguyenvien_url': reverse("admin:app_tinhnguyenvien_changelist"),
    }
    return render(request, 'home_index.html', context=context)
