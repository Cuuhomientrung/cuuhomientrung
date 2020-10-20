import django
import datetime
from django.db import models
from smart_selects.db_fields import ChainedForeignKey

RESOURCE_STATUS = [
    (1, 'Sẵn sàng'),
    (2, 'Không gọi được'),
    (3, 'Đang nghỉ/Hết tài nguyên'),
]

TINHNGUYEN_STATUS = [
    (1, 'Sẵn sàng'),
    (2, 'Không gọi được'),
    (3, 'Đang nghỉ'),
]

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
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thống kê Tỉnh"
        verbose_name_plural = "Thống kê Tỉnh"


class Huyen(models.Model):
    name = models.TextField(blank=True, default='', verbose_name="Huyện")
    tinh = models.ForeignKey(Tinh, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thống kê Huyện"
        verbose_name_plural = "Thống kê Huyện"


class Xa(models.Model):
    name = models.TextField(blank=True, default='', verbose_name="Xã")
    huyen = models.ForeignKey(Huyen, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thống kê Xã"
        verbose_name_plural = "Thống kê Xã"


class Thon(models.Model):
    name = models.TextField(blank=True, default='', verbose_name="Thôn")
    huyen = models.ForeignKey(Huyen, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thôn"
        verbose_name_plural = "Thôn"


class TinhNguyenVien(models.Model):
    name = models.TextField(blank=True, default='', verbose_name='Họ và tên')
    status = models.IntegerField(choices=TINHNGUYEN_STATUS, default=0, verbose_name="Tình trạng")
    location = models.TextField(blank=True, default='', verbose_name='Địa chỉ')
    phone = models.TextField(blank=True, default='', verbose_name='Điện thoại liên hệ')
    note = models.TextField(blank=True, default='', verbose_name='Ghi chú')

    tinh = models.ForeignKey(Tinh, blank=True, null=True, on_delete=models.CASCADE)
    huyen = models.ForeignKey(Huyen, blank=True, null=True, on_delete=models.CASCADE)
    xa = models.ForeignKey(Xa, blank=True, null=True, on_delete=models.CASCADE)
    thon = models.ForeignKey(Thon, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Tình nguyên viên thông tin'
        verbose_name_plural = 'Tình nguyên viên thông tin'


class CuuHo(models.Model):
    update_time = models.DateTimeField(auto_now=True, verbose_name='Cập nhật')
    name = models.TextField(blank=True, default='', verbose_name="Đội cứu hộ")

    status = models.IntegerField(choices=CUUHO_STATUS, default=0, verbose_name="Tình trạng")
    tinh = models.ForeignKey(
        Tinh, blank=True, null=True, on_delete=models.CASCADE,
        related_name="cuuho_reversed"
    )
    huyen = ChainedForeignKey(
        Huyen,
        chained_field="tinh",
        chained_model_field="tinh",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="cuuho_reversed"
    )
    xa = ChainedForeignKey(
        Xa,
        chained_field="huyen",
        chained_model_field="huyen",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="cuuho_reversed"
    )
    thon = ChainedForeignKey(
        Thon,
        chained_field="huyen",
        chained_model_field="huyen",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="cuuho_reversed"
    )
    location = models.TextField(blank=True, default='', verbose_name='Phạm vi cứu hộ')
    phone = models.TextField(blank=True, default='', verbose_name='Điện thoại liên hệ')
    note = models.TextField(blank=True, default='', verbose_name='Ghi chú')

    volunteer = models.ForeignKey(TinhNguyenVien, blank=True, null=True, verbose_name="Tình nguyện viên xác minh", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Các đội Cứu hộ'
        verbose_name_plural = 'Các đội Cứu hộ'


class HoDan(models.Model):
    name = models.TextField(blank=True, default='', verbose_name="Hộ dân")
    update_time = models.DateTimeField(auto_now=True, verbose_name='Cập nhật')
    location = models.TextField(blank=True, default='', verbose_name='Địa chỉ')
    status = models.IntegerField(choices=HODAN_STATUS, default=0, verbose_name="Tình trạng")
    tinh = models.ForeignKey(
        Tinh, blank=True, null=True, on_delete=models.CASCADE,
        related_name="hodan_reversed"
    )
    huyen = ChainedForeignKey(
        Huyen,
        chained_field="tinh",
        chained_model_field="tinh",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="hodan_reversed"
    )
    xa = ChainedForeignKey(
        Xa,
        chained_field="huyen",
        chained_model_field="huyen",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="hodan_reversed"
    )
    thon = ChainedForeignKey(
        Thon,
        chained_field="huyen",
        chained_model_field="huyen",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="hodan_reversed"
    )
    phone = models.TextField(blank=True, default='', verbose_name='Điện thoại liên hệ')
    note = models.TextField(blank=True, default='', verbose_name='Ghi chú')
    plus_code = models.TextField(blank=True, default='', verbose_name='Google Plus Code')
    volunteer = models.ForeignKey(TinhNguyenVien, blank=True, null=True, verbose_name="Tình nguyện viên xác minh", on_delete=models.CASCADE)
    cuuho = models.ForeignKey(CuuHo, null=True, blank= True, verbose_name="Đơn vị cứu hộ tiếp cận", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hộ dân cần ứng cứu'
        verbose_name_plural = 'Hộ dân cần ứng cứu'


class NguonLuc(models.Model):
    name = models.TextField(blank=True, default='', verbose_name="Nguồn lực")
    update_time = models.DateTimeField(auto_now=True, verbose_name='Cập nhật')
    location = models.TextField(blank=True, default='', verbose_name='Địa chỉ')
    status = models.IntegerField(choices=RESOURCE_STATUS, default=0, verbose_name="Tình trạng")

    tinh = models.ForeignKey(Tinh, blank=True, null=True, on_delete=models.CASCADE)
    huyen = models.ForeignKey(Huyen, blank=True, null=True, on_delete=models.CASCADE)
    xa = models.ForeignKey(Xa, blank=True, null=True, on_delete=models.CASCADE)
    thon = models.ForeignKey(Thon, blank=True, null=True, on_delete=models.CASCADE)

    phone = models.TextField(blank=True, default='', verbose_name='Điện thoại liên hệ')
    note = models.TextField(blank=True, default='', verbose_name='Ghi chú')

    volunteer = models.ForeignKey(TinhNguyenVien, blank=True, null=True, verbose_name="Tình nguyện viên xác minh", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Nguồn trợ giúp khác"
        verbose_name = "Nguồn trợ giúp khác"


class TinTuc(models.Model):
    title = models.TextField(blank=True, default='', verbose_name = "Tin")
    url = models.TextField(blank=True, default='', verbose_name = "Link")
    update_time = models.DateTimeField(auto_now=True, verbose_name='Cập nhật')
    note = models.TextField(blank=True, default='', verbose_name='Ghi chú')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Tin tức quan trọng "
        verbose_name = "Tin tức quan trọng "
