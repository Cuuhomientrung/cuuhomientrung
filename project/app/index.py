from app.admin import TinhAdmin
from app.models import Tinh, HoDan, CuuHo
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse


def index(request):
    tong_hodan_cap_cuu= HoDan.objects.filter(status_id=3).count()
    tong_doi_cuu_ho = CuuHo.objects.count()

    totalByTinh = Tinh.objects.prefetch_related('hodan_reversed')\
        .filter(hodan_reversed__status=1)\
        .annotate(total_hodan=Count("hodan_reversed"))\
        .annotate(total_cuuho=Count("cuuho_reversed"))\
        .order_by('-total_hodan')[0:5]
    hodanurl = reverse("admin:app_hodan_changelist")
    cuuhourl=reverse("admin:app_cuuho_changelist")
    tinhInfos = [
        {
            "url": f'{hodanurl}?{TinhAdmin.URL_CUSTOM_TAG}={tinh.pk}&status_id=3',
            "total_hodan": tinh.total_hodan,
            "total_cuuho": tinh.total_cuuho,
            "id": tinh.pk,
            "name": tinh.name
        } for tinh in totalByTinh
    ]

    context = {
        'tong_hodan_cap_cuu': tong_hodan_cap_cuu,
        'tong_doi_cuu_ho': tong_doi_cuu_ho,
        'tinhInfos': tinhInfos,
        'hodan_url' : hodanurl,
        'them_hodan_url': reverse("admin:app_hodan_add"),
        'them_cuuho_url': reverse("admin:app_cuuho_add"),
        'cuuho_url': cuuhourl,
    }
    return render(request, 'home_index.html', context=context)
