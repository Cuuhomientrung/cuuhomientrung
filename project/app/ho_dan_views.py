from django.http import HttpResponse
from django.shortcuts import render
from app.models import HoDan, HODAN_STATUS

def get_ho_dan():
    return HoDan.objects.all()

def index(request):
    list_ho_dan = get_ho_dan()
    status_dict = dict(HODAN_STATUS)
    context = {
        'list_ho_dan': [
            {
                'id': ho_dan.id,
                'name': ho_dan.name,
                'update_time': ho_dan.update_time,
                'tinh': ho_dan.tinh,
                'huyen': ho_dan.huyen,
                'xa': ho_dan.xa,
                'location': ho_dan.location,
                'status': status_dict[ho_dan.status],
                'people_number': ho_dan.people_number,
                'note': ho_dan.note,
            }
            for ho_dan in list_ho_dan
        ],
        'count': len(list_ho_dan),
        'trang_thai_dict': {
            0: "Chuaw",
            1: "ma",
        }
    }
    return render(request, 'ho_dan_index.html', context)
