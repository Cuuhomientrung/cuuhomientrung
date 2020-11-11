from django.db import models


class TinTuc(models.Model):
    title = models.TextField(blank=True, default="", verbose_name="Tin")
    url = models.TextField(blank=True, default="", verbose_name="Link")
    update_time = models.DateTimeField(auto_now=True, verbose_name="Cập nhật")
    note = models.TextField(blank=True, default="", verbose_name="Ghi chú")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Tin tức quan trọng "
        verbose_name = "Tin tức quan trọng "
