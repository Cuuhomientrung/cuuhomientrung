from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets
import datetime
from django.db.models import Q
from rest_framework.filters import SearchFilter
from rest_framework.permissions import DjangoModelPermissions
from django_restful_admin import RestFulModelAdmin
from rest_framework.response import Response
from app.models import HoDan, CuuHo, TinhNguyenVien, Tinh, Huyen, Xa, TrangThaiHoDan


class TinhHuyenXaBase(serializers.ModelSerializer):
    class Meta:
        abstract = True

    tinh = serializers.PrimaryKeyRelatedField(queryset=Tinh.objects.all())
    tinh_display = serializers.SerializerMethodField(read_only=True)
    huyen = serializers.PrimaryKeyRelatedField(queryset=Huyen.objects.all())
    huyen_display = serializers.SerializerMethodField(read_only=True)
    xa = serializers.PrimaryKeyRelatedField(queryset=Xa.objects.all())
    xa_display = serializers.SerializerMethodField(read_only=True)

    def get_tinh_display(self, obj):
        return obj.tinh.name if obj.tinh else ''

    def get_huyen_display(self, obj):
        return obj.huyen.name if obj.huyen else ''

    def get_xa_display(self, obj):
        return obj.xa.name if obj.xa else ''


class CuuHoSerializer(TinhHuyenXaBase):
    class Meta:
        model = CuuHo
        fields = '__all__'


class CuuHoViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = CuuHoSerializer
    queryset = CuuHo.objects.all()\
        .prefetch_related('tinh', 'huyen', 'xa')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'status', 'phone', 'location']
    search_fields = filterset_fields


class HoDanSerializer(TinhHuyenXaBase):
    status = serializers.PrimaryKeyRelatedField(queryset=TrangThaiHoDan.objects.all())
    status_display = serializers.SerializerMethodField(read_only=True)
    geo_longtitude = serializers.SerializerMethodField(read_only=True)
    geo_latitude = serializers.SerializerMethodField(read_only=True)
    update_time_timestamp = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CuuHo
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.status.name if obj.status else ''

    def get_geo_longtitude(self, obj):
        return obj.geo_location[0] if obj.geo_location else None

    def get_geo_latitude(self, obj):
        return obj.geo_location[1] if obj.geo_location else None

    def get_update_time_timestamp(self, obj):
        return int(obj.created_time.strftime("%s"))


class HoDanViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = HoDanSerializer
    queryset = HoDan.objects.all()\
        .prefetch_related('tinh', 'huyen', 'xa', 'status')\
        .order_by('-update_time')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'phone', 'location']
    search_fields = filterset_fields


class TinhNguyenVienSerializer(TinhHuyenXaBase):
    class Meta:
        model = TinhNguyenVien
        fields = '__all__'


class TinhNguyenVienViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = TinhNguyenVienSerializer
    queryset = TinhNguyenVien.objects.all()\
        .prefetch_related('tinh', 'huyen', 'xa')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'status', 'phone', 'location']
    search_fields = filterset_fields


class TinhSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tinh
        fields = '__all__'


class TinhViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = TinhSerializer
    queryset = Tinh.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    search_fields = filterset_fields


class HuyenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Huyen
        fields = '__all__'


class HuyenViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = HuyenSerializer
    queryset = Huyen.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    search_fields = filterset_fields


class TrangThaiHoDanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrangThaiHoDan
        fields = '__all__'


class TrangThaiHoDanSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = TrangThaiHoDanSerializer
    queryset = TrangThaiHoDan.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    search_fields = filterset_fields


class XaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xa
        fields = '__all__'


class XaViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = XaSerializer
    queryset = Xa.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    search_fields = filterset_fields


class BaseRestfulAdmin(RestFulModelAdmin):
    permission_classes = ()


class HoDanRestFulModelAdmin(BaseRestfulAdmin):

    def list(self, request):
        ten = request.GET.get("ten")
        phone = request.GET.get("phone")
        tinh = request.GET.get("tinh")
        huyen = request.GET.get("huyen")
        xa = request.GET.get("xa")
        status = request.GET.get("status")
        fromTime = request.GET.get("from")
        toTime = request.GET.get("to")

        if phone or tinh or huyen or status or fromTime or toTime or ten:
            filter = Q()
            if ten:
                operator = request.GET.get("ten_method")
                if operator == "contain":
                    filter = filter & Q(name__icontains=ten)
                else:
                    filter = filter & Q(name__iexact=ten)
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
