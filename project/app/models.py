from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from mapbox_location_field.models import LocationField
from simple_history.models import HistoricalRecords
from django.dispatch import receiver
from simple_history.signals import (
    post_create_historical_record
)

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
    tinh = models.ForeignKey(
        Tinh, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thống kê Huyện"
        verbose_name_plural = "Thống kê Huyện"


class Xa(models.Model):
    name = models.TextField(blank=True, default='', verbose_name="Xã")
    huyen = models.ForeignKey(
        Huyen, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thống kê Xã"
        verbose_name_plural = "Thống kê Xã"


class Thon(models.Model):
    name = models.TextField(blank=True, default='', verbose_name="Thôn")
    huyen = models.ForeignKey(
        Huyen, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thôn"
        verbose_name_plural = "Thôn"


class TinhNguyenVien(models.Model):
    name = models.TextField(blank=True, default='', verbose_name='Họ và tên')
    status = models.IntegerField(
        choices=TINHNGUYEN_STATUS, default=0, verbose_name="Tình trạng")
    location = models.TextField(blank=True, default='', verbose_name='Địa chỉ')
    phone = models.TextField(blank=True, default='',
                             verbose_name='Điện thoại liên hệ')
    note = models.TextField(blank=True, default='', verbose_name='Ghi chú')

    tinh = models.ForeignKey(
        Tinh, blank=True, null=True, on_delete=models.CASCADE)
    huyen = models.ForeignKey(
        Huyen, blank=True, null=True, on_delete=models.CASCADE)
    xa = models.ForeignKey(Xa, blank=True, null=True, on_delete=models.CASCADE)
    thon = models.ForeignKey(
        Thon, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tình nguyên viên thông tin'
        verbose_name_plural = 'Tình nguyên viên thông tin'


class CuuHo(models.Model):
    update_time = models.DateTimeField(auto_now=True, verbose_name='Cập nhật')
    name = models.TextField(blank=True, default='', verbose_name="Đội cứu hộ")
    status = models.IntegerField(
        choices=CUUHO_STATUS, default=0, verbose_name="Tình trạng")
    tinh = models.ForeignKey(
        Tinh, blank=True, null=True, on_delete=models.CASCADE,
        related_name="cuuho_reversed"
    )
    huyen = models.ForeignKey(
        Huyen,
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="cuuho_reversed"
    )
    xa = models.ForeignKey(
        Xa,
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="cuuho_reversed"
    )
    thon = models.ForeignKey(
        Thon,
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="cuuho_reversed"
    )
    location = models.TextField(
        blank=True, default='', verbose_name='Phạm vi cứu hộ')
    phone = models.TextField(blank=True, default='',
                             verbose_name='Điện thoại liên hệ')
    note = models.TextField(blank=True, default='', verbose_name='Ghi chú')

    volunteer = models.ForeignKey(TinhNguyenVien, blank=True, null=True,
                                  verbose_name="Tình nguyện viên xác minh", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Các đội Cứu hộ'
        verbose_name_plural = 'Các đội Cứu hộ'

    def save(self, *args, **kwargs):
        # Auto update huyen
        if self.xa and self.xa.pk:
            if self.xa.huyen and self.xa.huyen.pk:
                self.huyen = self.xa.huyen

        # Auto update tinh
        if self.huyen and self.huyen.pk:
            if self.huyen.tinh and self.huyen.tinh.pk:
                self.tinh = self.huyen.tinh

        super().save(*args, **kwargs)


class CustomLocationField(LocationField):
    pass


class IPAddressHistoricalModel(models.Model):
    """
    Abstract model for history models tracking the IP address.
    """
    ip_address = models.GenericIPAddressField(
        name='ip_address', blank=True, null=True
    )

    class Meta:
        abstract = True


class HoDan(models.Model):
    name = models.TextField(blank=True, default='', verbose_name="Hộ dân")
    update_time = models.DateTimeField(auto_now=True, verbose_name='Cập nhật')
    location = models.TextField(blank=True, default='', verbose_name='Địa chỉ')
    status = models.IntegerField(
        choices=HODAN_STATUS, default=0, verbose_name="Tình trạng")
    people_number = models.PositiveIntegerField(
        blank=True, null=True, default=1, verbose_name="Số người")
    tinh = models.ForeignKey(
        Tinh, blank=True, null=True, on_delete=models.CASCADE,
        related_name="hodan_reversed"
    )
    huyen = models.ForeignKey(
        Huyen,
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="hodan_reversed"
    )
    xa = models.ForeignKey(
        Xa,
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="hodan_reversed"
    )
    thon = models.ForeignKey(
        Thon,
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="hodan_reversed"
    )
    phone = models.TextField(blank=True, default='',
                             verbose_name='Điện thoại liên hệ')
    note = models.TextField(blank=True, default='', verbose_name='Ghi chú')
    volunteer = models.ForeignKey(TinhNguyenVien, blank=True, null=True,
                                  verbose_name="Tình nguyện viên xác minh", on_delete=models.CASCADE)
    cuuho = models.ForeignKey(CuuHo, null=True, blank=True,
                              verbose_name="Đơn vị cứu hộ tiếp cận", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=True, verbose_name='Ngày tạo')
    geo_location = CustomLocationField(null=True, blank=True)
    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True),
        bases=[IPAddressHistoricalModel, ]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hộ dân cần ứng cứu'
        verbose_name_plural = 'Hộ dân cần ứng cứu'

    def save(self, *args, **kwargs):
        # Auto update huyen
        if self.xa and self.xa.pk:
            if self.xa.huyen and self.xa.huyen.pk:
                self.huyen = self.xa.huyen

        # Auto update tinh
        if self.huyen and self.huyen.pk:
            if self.huyen.tinh and self.huyen.tinh.pk:
                self.tinh = self.huyen.tinh

        super().save(*args, **kwargs)


# TODO: update ip from user
# Find a better way to get ip latter
@receiver(post_create_historical_record)
def post_create_historical_record_callback(sender, **kwargs):
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    history_instance = kwargs['history_instance']
    # thread.request for use only when the simple_history middleware is on and enabled
    history_instance.ip_address = get_client_ip(
        HistoricalRecords.thread.request)
    if history_instance.ip_address:
        history_instance.save(update_fields=['ip_address', ])


class NguonLuc(models.Model):
    name = models.TextField(blank=True, default='', verbose_name="Nguồn lực")
    update_time = models.DateTimeField(auto_now=True, verbose_name='Cập nhật')
    location = models.TextField(blank=True, default='', verbose_name='Địa chỉ')
    status = models.IntegerField(
        choices=RESOURCE_STATUS, default=0, verbose_name="Tình trạng")

    tinh = models.ForeignKey(
        Tinh, blank=True, null=True, on_delete=models.CASCADE)
    huyen = models.ForeignKey(
        Huyen, blank=True, null=True, on_delete=models.CASCADE)
    xa = models.ForeignKey(Xa, blank=True, null=True, on_delete=models.CASCADE)
    thon = models.ForeignKey(
        Thon, blank=True, null=True, on_delete=models.CASCADE)

    phone = models.TextField(blank=True, default='',
                             verbose_name='Điện thoại liên hệ')
    note = models.TextField(blank=True, default='', verbose_name='Ghi chú')

    volunteer = models.ForeignKey(TinhNguyenVien, blank=True, null=True,
                                  verbose_name="Tình nguyện viên xác minh", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Nguồn trợ giúp khác"
        verbose_name = "Nguồn trợ giúp khác"


class TinTuc(models.Model):
    title = models.TextField(blank=True, default='', verbose_name="Tin")
    url = models.TextField(blank=True, default='', verbose_name="Link")
    update_time = models.DateTimeField(auto_now=True, verbose_name='Cập nhật')
    note = models.TextField(blank=True, default='', verbose_name='Ghi chú')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Tin tức quan trọng "
        verbose_name = "Tin tức quan trọng "
