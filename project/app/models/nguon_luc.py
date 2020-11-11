from django.db import models

from .status import ResourceStatus


class NguonLuc(models.Model):
    name = models.TextField(blank=True, default="", verbose_name="Nguồn lực")
    update_time = models.DateTimeField(auto_now=True, verbose_name="Cập nhật")
    location = models.TextField(blank=True, default="", verbose_name="Địa chỉ")
    status = models.IntegerField(
        choices=ResourceStatus.choices,
        default=ResourceStatus.READY,
        verbose_name="Tình trạng",
    )

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

    phone = models.TextField(blank=True, default="", verbose_name="Điện thoại liên hệ")
    note = models.TextField(blank=True, default="", verbose_name="Ghi chú")

    volunteer = models.ForeignKey(
        "app.TinhNguyenVien",
        blank=True,
        null=True,
        verbose_name="Tình nguyện viên xác minh",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Nguồn trợ giúp khác"
        verbose_name = "Nguồn trợ giúp khác"
