from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import HoDan, Tinh, Huyen, Xa, HODAN_STATUS_NEW

def get_ho_dan(status=None, tinh=None, huyen=None, xa=None):
    print (status, tinh, huyen, xa)
    query = HoDan.objects
    if status:
        query = query.filter(status=status)
    if tinh:
        query = query.filter(tinh=tinh)
    if huyen:
        query = query.filter(huyen=huyen)
    if xa:
        query = query.filter(xa=xa)
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
    return Tinh.objects.all()

def get_huyen():
    return Huyen.objects.all()

def get_xa():
    return Xa.objects.all()

PAGE_SIZE = 20

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

    list_dict_ho_dan = [{
        'id': ho_dan.id,
        'name': ho_dan.name,
        'created_time': ho_dan.created_time,
        'update_time': ho_dan.update_time,
        'tinh': ho_dan.tinh,
        'huyen': ho_dan.huyen,
        'xa': ho_dan.xa,
        'location': ho_dan.location,
        'status': ho_dan.status,
        'status_emergency': ho_dan.status.id in [3, 5, 6] if ho_dan.status,
        'people_number': ho_dan.people_number,
        'note': ho_dan.note,
        'phone': ho_dan.phone,
        'volunteer': ho_dan.volunteer,
        'cuuho': ho_dan.cuuho,
        'geo_location': ho_dan.geo_location,
    } for ho_dan in list_ho_dan]

    paginator = Paginator(list_dict_ho_dan, PAGE_SIZE)
    page_obj = paginator.get_page(page_number)
    return render(request, 'ho_dan_index.html', {
        'page_obj': page_obj,
        'status_dict': dict(HODAN_STATUS_NEW),
        'list_tinh': get_tinh(),
        'list_huyen': get_huyen(),
        'list_xa': get_xa(),
        'params_url': build_params_url(status, tinh, huyen, xa),
        'filtered': {
            'status': status,
            'tinh': tinh,
            'huyen': huyen,
            'xa': xa,
        },
    })
