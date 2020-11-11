from django.dispatch import receiver
from django.conf import settings

from rest_framework.authtoken.models import Token as BaseTokenClass
from simple_history.signals import post_create_historical_record
from simple_history.models import HistoricalRecords

from .status import *
from .locations import *
from .hodan import *
from .cuu_ho import *
from .volunteer import *
from .nguon_luc import NguonLuc
from .tin_tuc import TinTuc


__all__ = [
    "NguonLuc",
    "TinTuc",
    "Token",
    "post_create_historical_record_callback",
    "Tinh",
    "Huyen",
    "Xa",
    "Thon",
    "CustomLocationField",
    "TrangThaiHoDan",
    "HoDan",
    "CuuHo",
    "TinhNguyenVien",
    "ResourceStatus",
    "RescueStatus",
    "VolunteerStatus",
]


class Token(BaseTokenClass):
    class Meta:
        abstract = "rest_framework.authtoken" not in settings.INSTALLED_APPS


# TODO: update ip from user
# Find a better way to get ip latter
@receiver(post_create_historical_record)
def post_create_historical_record_callback(sender, **kwargs):
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    history_instance = kwargs["history_instance"]
    # thread.request for use only when the simple_history middleware is on and enabled
    try:
        history_instance.ip_address = get_client_ip(HistoricalRecords.thread.request)
        if history_instance.ip_address:
            history_instance.save(
                update_fields=[
                    "ip_address",
                ]
            )
    except:
        pass
