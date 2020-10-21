import os
import pprint
import datetime
from rest_framework import serializers, viewsets
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django_restful_admin import RestFulModelAdmin
from rest_framework.response import Response
from app.models import HoDan, Tinh
from app import models
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from app.forms import UploadFileForm, ConfirmationForm
from app.utils.importer import storage, parser


class BaseRestfulAdmin(RestFulModelAdmin):
    permission_classes = ()


class HoDanRestFulModelAdmin(BaseRestfulAdmin):
    def list(self, request):
        phone = request.GET.get("phone")
        tinh = request.GET.get("tinh")
        huyen = request.GET.get("huyen")
        xa = request.GET.get("xa")
        status = request.GET.get("status")
        fromTime = request.GET.get("from")
        toTime = request.GET.get("to")

        if phone or tinh or huyen or status or fromTime or toTime:
            filter = Q()
            if phone:
                filter = filter & Q(phone=phone)
            if tinh:
                filter = filter & Q(tinh=tinh)
            if huyen:
                filter = filter & Q(huyen=huyen)
            if xa:
                filter = filter & Q(xa=xa)
            if status:
                filter = filter & Q(status=status)
            if fromTime and toTime:
                start = datetime.datetime.strptime(
                    fromTime, "%Y-%m-%d-%H-%M-%S")
                end = datetime.datetime.strptime(toTime, "%Y-%m-%d-%H-%M-%S")
                filter = filter & Q(update_time__range=(start, end))

            queryset = HoDan.objects.filter(filter)
        else:
            # all if no filter
            queryset = HoDan.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# /import_table/, /confirm_import_table/


MSG_INVALID_METHOD = 'Chỉ cho phép thao tác GET và POST'
MSG_UNSUPPORTED_FILE = 'Đuôi file không hợp lệ'
SUPPORTED_FILE_EXT_LIST = ['.xlsx']


def handle_uploaded_file(f):
    file_path = storage.get_temp_file_path()
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return storage.file_path_to_file_name(file_path)


def is_supported_file(name):
    ext = os.path.splitext(name)[1].lower()
    return ext in SUPPORTED_FILE_EXT_LIST


def import_table(request):
    error_message = None

    if request.method == 'GET':
        form = UploadFileForm()
    elif request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if is_supported_file(file.name):
                file_name = handle_uploaded_file(file)
                return HttpResponseRedirect('/confirm_import_table/{}/'.format(file_name))
            else:
                error_message = MSG_UNSUPPORTED_FILE
    else:
        return HttpResponseNotAllowed(MSG_INVALID_METHOD)

    return render(request, 'app/import_table_form.html', {'form': form, 'error_message': error_message})


def confirm_import_table(request, uploaded_file_name):
    validation_result = parser.validate_import_table(uploaded_file_name)

    if request.method == 'GET':
        form = ConfirmationForm()
    elif request.method == 'POST':
        if not validation_result.error:
            hodan_list = validation_result.data["hodan_list"]
            HoDan.objects.bulk_create(hodan_list)
            return HttpResponse("Thành công!")
    else:
        return HttpResponseNotAllowed(MSG_INVALID_METHOD)

    return render(request, 'app/confirm_import_table_form.html', {
        'form': form,
        'action': '/confirm_import_table/{}/'.format(uploaded_file_name),
        'error': validation_result.error,
        'error_message': validation_result.error_message,
        'error_info': pprint.pformat(validation_result.error_info),
        'hodan_list': (validation_result.data or {}).get("hodan_list", None)
    })
