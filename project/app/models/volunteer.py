from django.db import models

from .status import VolunteerStatus


__all__ = ["TinhNguyenVien"]


class TinhNguyenVien(models.Model):
    name = models.TextField(blank=True, default="", verbose_name="Họ và tên")
    status = models.IntegerField(
        choices=VolunteerStatus.choices,
        default=VolunteerStatus.UNVERIFIED,
        verbose_name="Tình trạng",
    )
    location = models.TextField(blank=True, default="", verbose_name="Địa chỉ")
    phone = models.TextField(blank=True, default="", verbose_name="Điện thoại liên hệ")
    note = models.TextField(blank=True, default="", verbose_name="Ghi chú")

    tinh = models.ForeignKey(
        "app.Tinh", blank=True, null=True, on_delete=models.CASCADE
    )
    huyen = models.ForeignKey(
        "app.Huyen", blank=True, null=True, on_delete=models.CASCADE
    )
    xa = models.ForeignKey("app.Xa", blank=True, null=True, on_delete=models.CASCADE)
    thon = models.ForeignKey(
        "app.Thon", blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tình nguyên viên thông tin"
        verbose_name_plural = "Tình nguyên viên thông tin"
