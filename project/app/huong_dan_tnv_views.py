from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

def index(request):
    hodanurl = reverse("admin:app_hodan_changelist")
    cuuhourl=reverse("admin:app_cuuho_changelist")

    return render(request, 'huong_dan_tnv.html', {
        'hodan_url' : hodanurl,
        'cuuho_url': cuuhourl,
    })
