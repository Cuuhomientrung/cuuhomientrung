from app.admin import TinhAdmin
from app.models import Tinh, HoDan, CuuHo
from django.db.models import Count
from django.shortcuts import render


def index(request):
    tong_hodan_cap_cuu= HoDan.objects.filter(status_id=3).count()
    tong_doi_cuu_ho = CuuHo.objects.count()
    
    totalByTinh = Tinh.objects.prefetch_related('hodan_reversed')\
        .filter(hodan_reversed__status=1)\
        .annotate(total_hodan=Count("hodan_reversed"))\
        .order_by('-total_hodan')[0:5]
    tinhInfos = [
        {
            "url": f'/app/hodan/?{TinhAdmin.URL_CUSTOM_TAG}={tinh.pk}&status_id=3',
            "total_hodan": tinh.total_hodan,
            "id": tinh.pk,
            "name": tinh.name
        } for tinh in totalByTinh
    ]



    context = {
        'tong_hodan_cap_cuu': tong_hodan_cap_cuu,
        'tong_doi_cuu_ho': tong_doi_cuu_ho,
        'tinhInfos': tinhInfos,
        'hodan_url' : '/app/hodan/',
        'cuuho_url': '/app/cuuho/',
    }
    return render(request, 'index.html', context=context)