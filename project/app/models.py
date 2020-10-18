import django
import datetime
from django.db import models
from app.lib.utils import check_contain_filter


CUUHO_STATUS = [
    (0, 'Chưa xác minh'),
    (1, 'Sẵn sàng'),
    (2, 'Không gọi được'),
    (3, 'Đang cứu hộ'),
    (4, 'Đang nghỉ'),
]

HODAN_STATUS = [
    (0, "Chưa xác minh"),
    (1, "Cần ứng cứu gấp"),
    (2, "Không gọi được"),
    (3, "Đã được cứu"),
    (4, "Gặp nạn")
]

class Tinh(models.Model):
    name = models.TextField(blank=True, default='', verbose_name="Tỉnh")

class Huyen(models.Model):
    name = models.TextField(blank=True, default='', verbose_name="Huyện")

class Xa(models.Model):
    name = models.TextField(blank=True, default='', verbose_name="Xã")

class Thon(models.Model):
    name = models.TextField(blank=True, default='', verbose_name="Thôn")

class TinhNguyenVien(models.Model):
    name = models.TextField(blank=True, default='', verbose_name='Họ và tên')
    location = models.TextField(blank=True, default='', verbose_name='Địa chỉ')
    phone = models.TextField(blank=True, default='', verbose_name='Điện thoại liên hệ')
    note = models.TextField(blank=True, default='', verbose_name='Ghi chú')

    tinh = models.ForeignKey(Tinh, null=True)
    huyen = models.ForeignKey(Huyen, null=True)
    xa = models.ForeignKey(Xa, null=True)
    thon = models.ForeignKey(Thon, null=True)

class CuuHo(models.Model): 
    name = models.TextField(blank=True, default='', verbose_name="Đội cứu hộ")
    status = models.IntegerField(choices=CUUHO_CHOICES, default=0, verbose_name="Tình trạng")
    tinh = models.ForeignKey(Tinh, null=True)
    huyen = models.ForeignKey(Huyen, null=True)
    xa = models.ForeignKey(Xa, null=True)
    thon = models.ForeignKey(Thon, null=True)

    location = models.TextField(blank=True, default='', verbose_name='Phạm vi cứu hộ')
    phone = models.TextField(blank=True, default='', verbose_name='Điện thoại liên hệ')
    note = models.TextField(blank=True, default='', verbose_name='Ghi chú')

    volunteer = models.ForeignKey(TinhNguyenVien, null=True, verbose_name="Tình nguyện viên xác minh")

  
    