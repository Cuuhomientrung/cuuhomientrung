from django.db import models
from django.contrib.postgres.fields import ArrayField

from smart_selects.db_fields import ChainedForeignKey
from simple_history.models import HistoricalRecords

from .locations import CustomLocationField
from .status import Importances, CommunicationStatus
from ..utils.phone_number import export_phone_numbers

__all__ = ["TrangThaiHoDan", "HoDan"]


class IPAddressHistoricalModel(models.Model):
    """
    Abstract model for history models tracking the IP address.
    """

    ip_address = models.GenericIPAddressField(name="ip_address", blank=True, null=True)

    class Meta:
        abstract = True


class TrangThaiHoDan(models.Model):
    name = models.TextField(blank=True, default="", verbose_name="Tên trạng thái")
    created_time = models.DateTimeField(auto_now=True, verbose_name="Ngày tạo")
    update_time = models.DateTimeField(auto_now=True, verbose_name="Cập nhật")

    def __str__(self):
        return "%s" % (self.name)

    def __unicode__(self):
        return u"%s" % (self.name)


class HoDan(models.Model):
    name = models.TextField(blank=True, default="", verbose_name="Hộ dân")
    update_time = models.DateTimeField(auto_now=True, verbose_name="Cập nhật")
    location = models.TextField(blank=True, default="", verbose_name="Địa chỉ")
    status = models.ForeignKey(
        "app.TrangThaiHoDan",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        default=1,
        verbose_name="Trạng thái",
    )
    people_number = models.PositiveIntegerField(
        blank=True, null=True, default=1, verbose_name="Số người"
    )
    tinh = models.ForeignKey(
        "app.Tinh",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="hodan_reversed",
    )
    huyen = ChainedForeignKey(
        "app.Huyen",
        chained_field="tinh",
        chained_model_field="tinh",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True,
        null=True,
        related_name="hodan_reversed",
        on_delete=models.CASCADE,
    )

    xa = ChainedForeignKey(
        "app.Xa",
        chained_field="huyen",
        chained_model_field="huyen",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True,
        null=True,
        related_name="hodan_reversed",
        on_delete=models.CASCADE,
    )

    thon = models.ForeignKey(
        "app.Thon",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="hodan_reversed",
    )
    phone = models.TextField(blank=True, default="", verbose_name="Điện thoại liên hệ")
    phone_expored = models.TextField(
        blank=True,
        default="",
    )
    note = models.TextField(blank=True, default="", verbose_name="Ghi chú")
    volunteer = models.ForeignKey(
        "app.TinhNguyenVien",
        blank=True,
        null=True,
        verbose_name="Tình nguyện viên xác minh",
        on_delete=models.CASCADE,
    )
    cuuho = models.ForeignKey(
        "app.CuuHo",
        null=True,
        blank=True,
        verbose_name="Đơn vị cứu hộ tiếp cận",
        on_delete=models.CASCADE,
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    geo_location = CustomLocationField(null=True, blank=True)
    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True),
        bases=[
            IPAddressHistoricalModel,
        ],
    )
    do_quan_trong = models.TextField(
        choices=Importances.choices,
        default=Importances.IMPORTANT,
        help_text="Mức độ quan trọng",
        verbose_name="Độ quan trọng"
    )
    trang_thai_lien_lac = models.IntegerField(
        choices=CommunicationStatus.choices,
        default=CommunicationStatus.UNKNOWN,
        help_text="Tình trạng liên lạc của hộ dân",
        verbose_name="Trạng Thái Liên Lạc"
    )
    nhu_cau = ArrayField(
        models.TextField(),
        blank=True,
        null=True,
        help_text="Danh sách nhu cầu cần thiết của hộ dân. Dùng dấu phẩy để ngăn cách các nhu cầu",
        verbose_name="Danh sách nhu cầu",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hộ dân cần ứng cứu"
        verbose_name_plural = "Hộ dân cần ứng cứu"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        # Craw then export phone number before commit to database
        self.phone_expored = export_phone_numbers(self.phone)

        # Save as normal
        super().save(force_insert, force_update, using, update_fields)
