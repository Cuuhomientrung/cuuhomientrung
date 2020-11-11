from django.db import models

from mapbox_location_field.models import LocationField

__all__ = ["Tinh", "Huyen", "Xa", "Thon", "CustomLocationField"]


class CustomLocationField(LocationField):
    pass


class Tinh(models.Model):
    name = models.TextField(blank=True, default="", verbose_name="Tỉnh")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thống kê Tỉnh"
        verbose_name_plural = "Thống kê Tỉnh"


class Huyen(models.Model):
    name = models.TextField(blank=True, default="", verbose_name="Huyện")
    tinh = models.ForeignKey(Tinh, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thống kê Huyện"
        verbose_name_plural = "Thống kê Huyện"


class Xa(models.Model):
    name = models.TextField(blank=True, default="", verbose_name="Xã")
    huyen = models.ForeignKey(Huyen, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thống kê Xã"
        verbose_name_plural = "Thống kê Xã"


class Thon(models.Model):
    name = models.TextField(blank=True, default="", verbose_name="Thôn")
    huyen = models.ForeignKey(Huyen, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thôn"
        verbose_name_plural = "Thôn"
