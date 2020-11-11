from django.db import models

from smart_selects.db_fields import ChainedForeignKey

from .status import RescueStatus


__all__ = ["CuuHo"]


class CuuHo(models.Model):
    update_time = models.DateTimeField(auto_now=True, verbose_name="Cập nhật")
    name = models.TextField(blank=True, default="", verbose_name="Đội cứu hộ")
    status = models.IntegerField(
        choices=RescueStatus.choices,
        default=RescueStatus.UNVERIFIED,
        verbose_name="Tình trạng",
    )
    tinh = models.ForeignKey(
        "app.Tinh",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="cuuho_reversed",
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
        related_name="cuuho_reversed",
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
        related_name="cuuho_reversed",
        on_delete=models.CASCADE,
    )

    thon = models.ForeignKey(
        "app.Thon",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="cuuho_reversed",
    )
    location = models.TextField(blank=True, default="", verbose_name="Phạm vi cứu hộ")
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
        verbose_name = "Các đội Cứu hộ"
        verbose_name_plural = "Các đội Cứu hộ"

    # def save(self, *args, **kwargs):
    #     # Auto update huyen
    #     if self.xa and self.xa.pk:
    #         if self.xa.huyen and self.xa.huyen.pk:
    #             self.huyen = self.xa.huyen

    #     # Auto update tinh
    #     if self.huyen and self.huyen.pk:
    #         if self.huyen.tinh and self.huyen.tinh.pk:
    #             self.tinh = self.huyen.tinh

    #     super().save(*args, **kwargs)
