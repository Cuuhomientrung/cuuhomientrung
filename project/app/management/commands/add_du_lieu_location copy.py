import datetime
import django
from django.core.management.base import BaseCommand
from app.models import Tinh, Huyen, Xa, Thon, HoDan
import requests
import json


def get_location_list(tinhs=['Quảng Bình', 'Quảng Trị', 'Hà Tĩnh', 'Huế']):
    """Tra ve danh sach ten huyen, xa, thon cua mot tinh"""
    url = 'https://thongtindoanhnghiep.co/api/city'
    ds_tinh = None
    result = requests.get(url, timeout=5)
    if result.status_code == 200:
        data = json.loads(result.text)
        ds_tinh = [{
            "id": x['ID'],
            "name": x['Title']
        }
            for x in data['LtsItem']
        ]
    else:
        print("Khong the lay danh sach tinh")
        return None

    ds_result = []
    for name in tinhs:  # xu ly tung tinh trong danh sach
        for tinh in ds_tinh:
            if name in tinh['name']:
                tinh_id = tinh['id']
                # get ds huyen
                url_tinh = f'https://thongtindoanhnghiep.co/api/city/{tinh_id}/district'
                ds_huyen = None
                result_tinh = requests.get(url_tinh, timeout=5)
                if result_tinh.status_code == 200:
                    data_tinh = json.loads(result_tinh.text)
                    ds_huyen = [
                        {
                            "id": x['ID'],
                            "name": x['Title']
                        }
                        for x in data_tinh
                    ]
                    ds_result.append(
                        {
                            'id': tinh['id'],
                            'name': tinh['name'],
                            'huyen': ds_huyen
                        }
                    )
                    # get ds xa
                    for huyen in ds_huyen:
                        huyen_id = huyen['id']
                        # get ds xa
                        url_huyen = f'https://thongtindoanhnghiep.co/api/district/{huyen_id}/ward'

                        result_huyen = requests.get(url_huyen, timeout=5)
                        if result_huyen.status_code == 200:
                            data_huyen = json.loads(result_huyen.text)
                            ds_xa = [
                                {
                                    "id": x['ID'],
                                    "name": x['Title']
                                }
                                for x in data_huyen
                            ]
                            huyen['xa'] = ds_xa
                else:
                    print(f"Khong the lay ds huyen cua tinh {tinh['name']}")

    return ds_result


class Command(BaseCommand):
    def handle(self, **options):
        """Add du lieu tinh, huyen, xa"""
        tinh_list = ['Quảng Bình', 'Quảng Trị', 'Huế']
        ds_result = get_location_list()
        for tinh in ds_result:
            tinh_name = tinh['name']

            tinh_obj = Tinh.objects.filter(
                name=tinh_name
            ).first()
            if not tinh_obj:
                tinh_obj = Tinh.objects.create(
                    name=tinh_name
                )
            else:
                for huyen in tinh['huyen']:
                    huyen_name = huyen['name']
                    huyen_obj = Huyen.objects.filter(
                        name=huyen_name
                    ).first()
                    if not huyen_obj:
                        huyen_obj = Huyen.objects.create(
                            name=huyen_name,
                            tinh=tinh_obj
                        )
                    else:
                        huyen_obj.tinh = tinh_obj
                        huyen_obj.name = huyen_name
                        huyen_obj.save()

                    for xa in huyen['xa']:
                        xa_name = xa['name']
                        xa_obj = Xa.objects.filter(
                            name=xa_name
                        ).first()

                        if not xa_obj:
                            xa_obj = Xa.objects.create(
                                name=xa_name,
                                huyen=huyen_obj
                            )
                        else:
                            xa_obj.name = xa_name
                            xa_obj.huyen = huyen_obj
                            xa_obj.save()
