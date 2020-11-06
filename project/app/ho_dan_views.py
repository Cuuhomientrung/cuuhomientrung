import json
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import HoDan, Tinh, Huyen, Xa, TrangThaiHoDan

def get_ho_dan(status=None, tinh=None, huyen=None, xa=None):
    query = HoDan.objects
    if status:
        query = query.filter(status=status)
    if tinh:
        query = query.filter(tinh=tinh)
    if huyen:
        query = query.filter(huyen=huyen)
    if xa:
        query = query.filter(xa=xa)
    query = query.prefetch_related('tinh', 'huyen', 'xa', 'status', 'volunteer')\
            .order_by('-update_time', 'id')
    return query.all()

def build_params_url(status=None, tinh=None, huyen=None, xa=None):
    url = "?"
    if status:
        url = url + "status=" + status + "&"
    if tinh:
        url = url + "tinh=" + tinh + "&"
    if huyen:
        url = url + "huyen=" + huyen + "&"
    if xa:
        url = url + "xa=" + xa + "&"
    return url

def get_tinh():
    return Tinh.objects.order_by('name').all()

def get_huyen(tinh_id=None):
    query = Huyen.objects.prefetch_related('tinh').order_by('name')
    if tinh_id:
        query = query.filter(tinh=tinh_id)
    return query.all()

def get_xa(huyen_id=None):
    query = Xa.objects.prefetch_related('huyen').order_by('name')
    if huyen_id:
        query = query.filter(huyen=huyen_id)
    return query.all()

def get_status():
    return TrangThaiHoDan.objects.all()

PAGE_SIZE = 20

def get_huyen_api(request):
    tinh = request.GET.get("tinh")
    list_huyen = get_huyen(tinh)
    dict_huyen = {
        huyen.id: huyen.name
        for huyen in list_huyen
    }
    return HttpResponse(json.dumps(dict_huyen), content_type="application/json")

def get_xa_api(request):
    huyen = request.GET.get("huyen")
    list_xa = get_xa(huyen)
    dict_xa = {
        xa.id: xa.name
        for xa in list_xa
    }
    return HttpResponse(json.dumps(dict_xa), content_type="application/json")

def index(request):
    status = request.GET.get("status")
    tinh = request.GET.get("tinh")
    huyen = request.GET.get("huyen")
    xa = request.GET.get("xa")
    page_number = request.GET.get('page')

    list_ho_dan = list(get_ho_dan(
        status=status,
        tinh=tinh,
        huyen=huyen,
        xa=xa,
    ))

    paginator = Paginator(list_ho_dan, PAGE_SIZE)
    page_obj = paginator.get_page(page_number)
    paged_list_ho_dan = page_obj.object_list
    paged_list_dict_ho_dan = [{
        'id': ho_dan.id,
        'name': ho_dan.name,
        'created_time': ho_dan.created_time,
        'update_time': ho_dan.update_time,
        'tinh': ho_dan.tinh,
        'huyen': ho_dan.huyen,
        'xa': ho_dan.xa,
        'location': ho_dan.location,
        'status': ho_dan.status,
        'status_emergency': (ho_dan.status.id in [3, 5, 6]) if ho_dan.status else False,
        'people_number': ho_dan.people_number,
        'note': ho_dan.note,
        'phone': ho_dan.phone,
        'volunteer': ho_dan.volunteer,
        'cuuho': ho_dan.cuuho,
        'geo_location': ho_dan.geo_location,
    } for ho_dan in paged_list_ho_dan]
    page_obj.object_list = paged_list_dict_ho_dan

    return render(request, 'ho_dan_index.html', {
        'page_obj': page_obj,
        'list_status': get_status(),
        'ho_dan_total_count': len(list_ho_dan),
        'list_tinh': get_tinh(),
        'list_huyen': get_huyen(tinh) if tinh else [],
        'list_xa': get_xa(huyen) if huyen else [],
        'params_url': build_params_url(status, tinh, huyen, xa),
        'filtered': {
            'status': status,
            'tinh': tinh,
            'huyen': huyen,
            'xa': xa,
        },
    })
