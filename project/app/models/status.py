from django.db import models

__all__ = ["ResourceStatus", "RescueStatus", "VolunteerStatus"]


class ResourceStatus(models.IntegerChoices):
    READY = 1, "Sẵn sàng"
    UNREACHABLE = 2, "Không gọi được"
    OUT_OF_RESOURCES = 3, "Đang nghỉ/Hết tài nguyên"


class VolunteerStatus(models.IntegerChoices):
    UNVERIFIED = 0, "Chưa xác minh"
    READY = 1, "Sẵn sàng"
    UNREACHABLE = 2, "Không gọi được"
    RESTING = 3, "Đang nghỉ"


class RescueStatus(models.IntegerChoices):
    UNVERIFIED = 0, "Chưa xác minh"
    READY = 1, "Sẵn sàng"
    UNREACHABLE = 2, "Không gọi được"
    NEED_HELP = 5, "Cần hỗ trợ"
    RESCUING = 3, "Đang cứu hộ"
    RESTING = 4, "Đang nghỉ"


class Importances(models.TextChoices):
    VERY_IMPORTANT = "P0", "Cực kỳ quan trọng"
    IMPORTANT = "P1", "Quan trọng"
    LESS_IMPORTANT = "P2", "Ít quan trọng"


class CommunicationStatus(models.IntegerChoices):
    UNKNOWN = 0, "Không rõ"
    UNREACHABLE = 1, "Không liên lạc được"
    REACHABLE = 2, "Liên lạc được"
