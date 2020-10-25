from app.admin import TinhAdmin
from app.models import Tinh, HoDan, CuuHo
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse


def index(request):
    tong_hodan_cap_cuu= HoDan.objects.filter(status_id__in=[3, 5, 6]).count()
    tong_hodan_da_duoc_cuu = HoDan.objects.filter(status_id=7).count()
    tong_doi_cuu_ho = CuuHo.objects.count()

    totalHoDanByTinh = Tinh.objects.prefetch_related('hodan_reversed')\
        .filter(hodan_reversed__status_id=3)\
        .annotate(total_hodan=Count("hodan_reversed"))\
        .order_by('-total_hodan')[0:5]
    cuuHoByTinh = Tinh.objects.prefetch_related('cuuho_reversed')\
        .annotate(total_cuuho=Count("cuuho_reversed"))\
        .filter(id__in=[tinh.id for tinh in totalHoDanByTinh])
    cuuHoDict = dict((o.id,o) for o in cuuHoByTinh)
    hodanurl = reverse("admin:app_hodan_changelist")
    cuuhourl=reverse("admin:app_cuuho_changelist")
    tinhInfos = [
        {
            "url": f'{hodanurl}?{TinhAdmin.URL_CUSTOM_TAG}={tinh.pk}&status_id=3',
            "total_hodan": tinh.total_hodan,
            "total_cuuho": cuuHoDict.get(tinh.id).total_cuuho,
            "id": tinh.pk,
            "name": tinh.name
        } for tinh in  totalHoDanByTinh
    ]

    context = {
        'tong_hodan_cap_cuu': tong_hodan_cap_cuu,
        'tong_hodan_da_duoc_cuu': tong_hodan_da_duoc_cuu,
        'tong_doi_cuu_ho': tong_doi_cuu_ho,
        'tinhInfos': tinhInfos,
        'hodan_url' : hodanurl,
        'them_hodan_url': reverse("admin:app_hodan_add"),
        'them_cuuho_url': reverse("admin:app_cuuho_add"),
        'cuuho_url': cuuhourl,
    }
    return render(request, 'home_index.html', context=context)
