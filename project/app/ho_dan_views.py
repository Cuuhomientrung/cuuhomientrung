from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import HoDan, HODAN_STATUS

def get_ho_dan():
    return HoDan.objects.all()

PAGE_SIZE = 20

def index(request):
    status_dict = dict(HODAN_STATUS)
    list_ho_dan = [{
        'id': ho_dan.id,
        'name': ho_dan.name,
        'created_time': ho_dan.created_time,
        'update_time': ho_dan.update_time,
        'tinh': ho_dan.tinh,
        'huyen': ho_dan.huyen,
        'xa': ho_dan.xa,
        'location': ho_dan.location,
        'status': ho_dan.status,
        'people_number': ho_dan.people_number,
        'note': ho_dan.note,
        'phone': ho_dan.phone,
        'volunteer': ho_dan.volunteer,
        'cuuho': ho_dan.cuuho,
        'geo_location': ho_dan.geo_location,
    } for ho_dan in list(get_ho_dan()) * 100]

    paginator = Paginator(list_ho_dan, PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ho_dan_index.html', {'page_obj': page_obj})
