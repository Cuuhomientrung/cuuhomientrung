from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import HoDan, HODAN_STATUS_NEW

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
    return query.all()

PAGE_SIZE = 20

def index(request):
    status = request.GET.get("status_id")
    tinh = request.GET.get("tinh")
    huyen = request.GET.get("huyen")
    xa = request.GET.get("xa")

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
        #TODO: fix here, not a good code
        'status_emergency': str(ho_dan.status) in [
            "Cần ứng cứu gấp",
            "Cần thức ăn",
            "Cần thuốc men",
        ],
        'people_number': ho_dan.people_number,
        'note': ho_dan.note,
        'phone': ho_dan.phone,
        'volunteer': ho_dan.volunteer,
        'cuuho': ho_dan.cuuho,
        'geo_location': ho_dan.geo_location,
    } for ho_dan in list_ho_dan]

    paginator = Paginator(list_dict_ho_dan, PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ho_dan_index.html', {
        'page_obj': page_obj,
        'status_dict': dict(HODAN_STATUS_NEW),
    })
