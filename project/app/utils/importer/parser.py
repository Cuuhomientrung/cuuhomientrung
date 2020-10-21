import django
import pandas
from app import models
from . import storage


ERROR_MESSAGE_INVALID_HEADERS = "Danh sách tiêu đề cột không hợp lệ"
ERROR_MESSAGE_UNKNOWN_ERROR = "Lỗi gì vậy ta?"


class ValidationError:
    NONE = 0
    INVALID_HEADERS = 1001
    INVALID_CONTENT = 1002
    UNKNOWN_ERROR = 2000


class Row:
    def __init__(self, name, status, location, tinh, huyen, xa, phone, note):
        self.name = name
        self.status = status
        self.location = location
        self.tinh = tinh
        self.huyen = huyen
        self.xa = xa
        self.phone = phone
        self.note = note


class Headers(Row):
    pass


class Info(Row):
    pass


class ValidationResult:
    def __init__(self, error=None, error_message=None, error_info=None, data=None, data_info=None):
        self.error = error
        self.error_message = error_message
        self.error_info = error_info
        self.data = data
        self.data_info = data_info


DEFAULT_HEADERS = Headers(
    name="Hộ dân",
    status="Tình trạng",
    location="Vị trí",
    tinh="Tỉnh",
    huyen="Huyện",
    xa="Xã",
    phone="Số điện thoại",
    note="Ghi chú",
)


def dict_to_hodan(d, headers=DEFAULT_HEADERS, create_when_missing=False):

    def get_foreign_key(manager: django.db.models.Manager, raw_name, default_value=None, **kwargs):
        if not raw_name:
            return default_value
        if manager.filter(name=raw_name, **kwargs).exists():
            return manager.get(name=raw_name, **kwargs)
        if create_when_missing:
            return manager.create(name=raw_name, **kwargs)
        raise Exception("Cannot find {} in {}".format(
            {"name": raw_name, **kwargs}, manager)
        )

    raw_name = d[headers.name] or ''
    raw_status = d[headers.status] or ''
    raw_location = d[headers.location] or ''
    raw_tinh = d[headers.tinh] or ''
    raw_huyen = d[headers.huyen] or ''
    raw_xa = d[headers.xa] or ''
    raw_phone = d[headers.phone] or ''
    raw_note = d[headers.note] or ''

    name = raw_name.strip()
    status = next((k for (k, v) in models.HODAN_STATUS if v == raw_status), 0)
    location = raw_location.strip()
    tinh = get_foreign_key(
        models.Tinh.objects, raw_tinh) if raw_tinh else None
    huyen = get_foreign_key(
        models.Huyen.objects, raw_huyen, tinh=tinh) if tinh else None
    xa = get_foreign_key(
        models.Xa.objects, raw_xa, huyen=huyen) if huyen else None
    phone = raw_phone.strip()
    note = raw_note.strip()

    result = models.HoDan(
        name=name,
        status=status,
        location=location,
        tinh=tinh,
        huyen=huyen,
        xa=xa,
        thon=None,
        phone=phone,
        volunteer=None,
        cuuho=None,
        update_time=None,
        note=note,
    )
    return result


# def get_dict_list_from_file_name(file_name):
#     file_path = storage.file_name_to_file_path(file_name)
#     df = pandas.read_excel(file_path, keep_default_na=False)
#     records = df.to_dict('records')
#     return records


def validate_import_table(file_name, headers=DEFAULT_HEADERS):
    df = pandas.read_excel(storage.file_name_to_file_path(
        file_name), dtype=str, keep_default_na=False)
    required_headers = [headers.name, headers.status, headers.location,
                        headers.tinh, headers.huyen, headers.xa, headers.phone, headers.note]
    actual_headers = list(df)

    if not set(required_headers).issubset(set(actual_headers)):
        return ValidationResult(error=ValidationError.INVALID_HEADERS, error_message=ERROR_MESSAGE_INVALID_HEADERS, error_info={
            "expected": required_headers,
            "actual": actual_headers,
            "missing": list(set(required_headers).difference(set(actual_headers)))
        })

    try:
        dict_list = df.to_dict('records')
        hodan_list = list(map(dict_to_hodan, dict_list))
    except Exception as e:
        return ValidationResult(error=ValidationError.UNKNOWN_ERROR, error_message=ERROR_MESSAGE_UNKNOWN_ERROR, error_info=e)

    return ValidationResult(data={
        'hodan_list': hodan_list
    })
