import json
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
import pygeohash as pgh
import sys
from django.core.paginator import Paginator
from app.models import HoDan, Tinh, Huyen, Xa, TrangThaiHoDan, HoDanLienLac, HoDanNhuCau, HoDanDoQuanTrong, TinhNguyenVien

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
            .order_by('-update_time', 'id').exclude(status=7)  # 7 is equa Hoan Thanh
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

#Get tinh by tinh_id
def get_tinh_by_id(tinh_id):
    return Tinh.objects.get(pk=tinh_id)

def get_huyen(tinh_id=None):
    query = Huyen.objects.prefetch_related('tinh').order_by('name')
    if tinh_id:
        query = query.filter(tinh=tinh_id)
    return query.all()

#Get huyen by huyen_id
def get_huyen_by_id(huyen_id):
    return Huyen.objects.get(pk=huyen_id)

def get_xa(huyen_id=None):
    query = Xa.objects.prefetch_related('huyen').order_by('name')
    if huyen_id:
        query = query.filter(huyen=huyen_id)
    return query.all()

#Get xa by huyen_id
def get_xa_by_id(xa_id):
    return Xa.objects.get(pk=xa_id)

def get_status():
    return TrangThaiHoDan.objects.order_by('trangthai_sort_index').filter(status=True)

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

def get_init_map_api(request):
    status = request.GET.get("status")
    tinh = request.GET.get("tinh")
    huyen = request.GET.get("huyen")
    xa = request.GET.get("xa")
    page_number = request.GET.get('page')

    list_ho_dan = get_ho_dan(
        status=status,
        tinh=tinh,
        huyen=huyen,
        xa=xa,
    )
    
    dict_hodan = [{'id': ho_dan.id,
        'name': ho_dan.name,
        'people_number': ho_dan.people_number,
        'status': ho_dan.status.id,
        'do_quan_trong': ho_dan.do_quan_trong.doquantrong_name,
        'marker_color': ho_dan.do_quan_trong.doquantrong_maker_color_code,
        'hodan_nhucau':ho_dan.hodan_nhucau.nhucau_name,
        'geo_lat_lon': ho_dan.geo_lat_lon} for ho_dan in list_ho_dan]

    return HttpResponse(json.dumps(dict_hodan), content_type="application/json")

def get_ho_dan_detail(request):
    try:
        hodan_id = int(request.GET.get("id"))
        ho_dan = HoDan.objects.get(pk=hodan_id)
        print(ho_dan.location)
        created_time = ho_dan.created_time
        created_time = created_time.strftime('%d/%m/%Y %H:%M')
        print(created_time)
        update_time = ho_dan.update_time
        update_time = update_time.strftime('%d/%m/%Y %H:%M')
        dict_hodan = {'id': ho_dan.id,
        'name': ho_dan.name,
        'people_number': ho_dan.people_number,
        'status': ho_dan.status.name,
        'note': ho_dan.note,
        'address': ho_dan.location+" ,"+(ho_dan.xa.name if ho_dan.xa else "")+" ,"+(ho_dan.huyen.name if ho_dan.huyen else "")+" ,"+(ho_dan.tinh.name if ho_dan.tinh else ""),
        'do_quan_trong': ho_dan.do_quan_trong.doquantrong_name,
        'marker_color': ho_dan.do_quan_trong.doquantrong_maker_color_code,
        'hodan_nhucau':ho_dan.hodan_nhucau.nhucau_name,
        'phone': ho_dan.phone,
        'created_time': created_time,
        'update_time': update_time,
        'volunteer': ho_dan.volunteer.name if ho_dan.volunteer else "",
        'cuuho': ho_dan.cuuho.name if ho_dan.cuuho else "",
        'geo_lat_lon': ho_dan.geo_lat_lon}
        print(ho_dan.geo_lat_lon)
        return HttpResponse(json.dumps(dict_hodan), content_type="application/json")
    except:
        print("get_ho_dan_detail: ", sys.exc_info()[0])
        error = {"status":"ERROR"}
        return HttpResponse(json.dumps(error), content_type="application/json")


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
        'geo_lat_lon': ho_dan.geo_lat_lon,
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


#NAME
#  pre_check_phone
#DESCRIPTION
#  api checking citizen's phone number
#INPUT:
#  request
#OUTPUT:
#  result{"status":"","data":[listofresult]}
#Created_By
# NGUYEN DUNG

def pre_check_phone(request, form_url='', extra_context=None):
        from django.http import JsonResponse
        from .views import HoDanSerializer
        result = {
            "response": False                # system err
            ,"data": ""                      # List of data for checking phone number
            ,"similar_hodan":""              #
            ,"status": False                 # There is no similar phone
        }
        try:
            # Build query string
            phone_numbers = request.GET.get('phone_numbers', '').split(',')
            current_object_id = request.GET.get('object_id', None)
            regex = '^.*(%s).*$' % '|'.join(phone_numbers)
            filter_query = {'phone_expored__iregex': regex}
            queryset = HoDan.objects.filter(**filter_query)
            if current_object_id:
                queryset = queryset.exclude(pk=current_object_id)

            hodans = HoDanSerializer(queryset, many=True)
            # Return json data (based on api serializers)
            result["response"] = True
            if queryset:
                result["data"]= hodans.data
                result["status"]= True
            return JsonResponse(result)
        except:
            # Return json data (based on api serializers)
            return JsonResponse(result)

#
IMPORTANCE_P0 = 0
def get_maker_color_by_import(importance):
    if importance == IMPORTANCE_P0 :
        return "blue"
    else:
        return "red"

#

def get_hodan_trang_thai(status):
    return TrangThaiHoDan.objects.get(pk=status)

def get_hodan_lienlac():
    return HoDanLienLac.objects.order_by('lienlac_sort_index').filter(lienlac_used_status=True)

def get_hodan_lienlac_id(lienlac_id):
    return HoDanLienLac.objects.get(pk=lienlac_id)

def get_hodan_doquantrong():
    return HoDanDoQuanTrong.objects.order_by('doquantrong_sort_index').filter(doquantrong_used_status=True)

def get_hodan_doquantrong_id(quantrong_id):
    return HoDanDoQuanTrong.objects.get(pk=quantrong_id)

def get_hodan_nhucau():
    return HoDanNhuCau.objects.order_by('nhucau_sort_index').filter(nhucau_used_status=True)

def get_hodan_nhucau_id(nhucau_id):
    return HoDanNhuCau.objects.get(pk=nhucau_id)

def get_hodan_doquantrong():
    return HoDanDoQuanTrong.objects.order_by('doquantrong_sort_index').filter(doquantrong_used_status=True)

def get_all_volunteer():
    return TinhNguyenVien.objects.order_by('name').all()

def get_hodan_volunteer_id(id):
    if id != -1:
        return TinhNguyenVien.objects.get(pk=id)
    else:
        return None

#NAME
#  add_ho_dan
#DESCRIPTION
#  View them moi mot ho dan
#INPUT:
#  request
#OUTPUT:
#
#Created_By
#  Dang_Hoang

def add_ho_dan(request):
    try:
        context = {
                "title":""
                ,"table":""
                ,"total":""
                ,'list_tinh': get_tinh()
                ,'list_huyen': []
                ,'list_xa': []
                ,'list_nhucau':get_hodan_nhucau()
                ,'list_lienlac':get_hodan_lienlac()
                ,'list_doquantrong':get_hodan_doquantrong()
                ,'list_status':get_status()
                ,'list_tinhnguyenvien':get_all_volunteer()
            }
        if request.POST:
            from mapbox_location_field.models import LocationField
            hodan_name = request.POST.get('hodan_name',"")
            hodan_phone = request.POST.get('hodan_phone',"")
            print(hodan_name)
            hodan_people = request.POST.get('hodan_people',"")
            hodan_status = int(request.POST.get('hodan_status',""))
            print(hodan_status)
            hodan_status = get_hodan_trang_thai(hodan_status)
            
            hodan_lienlac = int(request.POST.get('hodan_lienlac',"0"))
            print(hodan_lienlac)
            hodan_lienlac = get_hodan_lienlac_id(hodan_lienlac)
            
            hodan_doquantrong = int(request.POST.get('hodan_quantrong',"0"))
            hodan_doquantrong = get_hodan_doquantrong_id(hodan_doquantrong)
            hodan_nhucau = int(request.POST.get('hodan_nhucau',""))
            hodan_nhucau = get_hodan_nhucau_id(hodan_nhucau)
            hodan_nhucau_khac = request.POST.get('hodan_nhucau_khac',"")
            hodan_note = request.POST.get('hodan_note',"")
            print(hodan_note)
            hodan_tinh = int(request.POST.get('hodan_tinh',""))
            hodan_tinh = get_tinh_by_id(hodan_tinh)
            hodan_huyen = int(request.POST.get('hodan_huyen',""))
            hodan_huyen = get_huyen_by_id(hodan_huyen)
            hodan_xa = int(request.POST.get('hodan_xa',""))
            print(hodan_xa)
            hodan_xa = get_xa_by_id(hodan_xa)
            hodan_address = request.POST.get('hodan_address',"")
            hodan_geo_lat = float(request.POST.get('hodan_geo_lat',""))
            hodan_geo_lng = float(request.POST.get('hodan_geo_lng',""))
            print(hodan_geo_lat)
            hodan_volunteer = int(request.POST.get('hodan_tinhnguyenvien',"-1"))
            print(hodan_volunteer)
            hodan_volunteer = get_hodan_volunteer_id(hodan_volunteer)
            #marker_color = get_maker_color_by_import(hodan_import)
            #geo_location = LocationField(map_attrs={"center": [hodan_geo_lng,hodan_geo_lat], "marker_color": marker_color})
            geo_hash = pgh.encode(hodan_geo_lng,hodan_geo_lat)
            print(geo_hash)
            geo_data = {'geohash':geo_hash,'lat':hodan_geo_lat,'lng':hodan_geo_lng}
            
            hodan = HoDan(name=hodan_name
                          ,phone=hodan_phone
                          ,note = hodan_note
                          ,status=hodan_status
                          ,trang_thai_lien_lac= hodan_lienlac
                          ,do_quan_trong=hodan_doquantrong
                          ,hodan_nhucau= hodan_nhucau
                          ,hodan_nhucau_khac= hodan_nhucau_khac
                          ,people_number= hodan_people
                          ,volunteer=hodan_volunteer
                          ,location=hodan_address
                          ,tinh = hodan_tinh
                          ,huyen=hodan_huyen
                          ,xa = hodan_xa
                          ,geo_lat_lon=geo_data)
            hodan.save()
            messages.success(request,'Bạn đã thêm mới một hộ dân cần cứu hộ.')
            return redirect('home_ho_dan')
        else:
            return render(request, 'ho_dan_add.html',context)
    except:
        print("add_ho_dan error: ", sys.exc_info()[0])
        messages.warning(request, 'Đã có lỗi hệ thống xảy ra, vui lòng liên hệ admin.')
        return render(request, 'ho_dan_add.html')

def view_hodan(request):
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
        'geo_lat_lon': ho_dan.geo_lat_lon,
    } for ho_dan in paged_list_ho_dan]
    page_obj.object_list = paged_list_dict_ho_dan
    context = {
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
    }
    return render(request, 'ho_dan_view.html',context)
