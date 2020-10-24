import datetime
import django
from django.core.management.base import BaseCommand
from app.models import Tinh, Huyen, Xa, Thon, HoDan
import requests
import json


def is_vietnamese(name):
    accents = ['à', 'á', 'ạ', 'ả', 'ã', 'ó', 'ò', 'ỏ', 'ọ', 'õ', 'ô', 'ồ', 'ố', 'ổ', 'ộ', 'ơ', 'ờ', 'ớ', 'ở', 'ợ', 'ê',
               'ề', 'ế', 'ể', 'ệ', 'ì', 'í', 'ỉ', 'ị', 'ù', 'ú', 'ụ', 'ủ', 'ư', 'ừ', 'ú', 'ủ', 'ự', 'ữ', 'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ']
    is_vietnamese = False
    for ch in accents:
        if ch in name:
            is_vietnamese = True
            break
    return is_vietnamese


def has_special_character(name):
    accents = [':', '?', '_', '@',
               '(', ')', '/', '.', '$', '<', '>', '!', 'lxbfYeaa']
    is_special = False
    for ch in accents:
        if ch in name:
            is_special = True
            break
    return is_special


class Command(BaseCommand):
    def handle(self, **options):
        """Xoa du lieu bi spam vao database"""

        for tinh in Tinh.objects.all():
            if not is_vietnamese(tinh.name):
                if has_special_character(tinh.name):
                    tinh.delete()
                else:
                    choice = input(
                        f"Do you want to delete {tinh.name} ? (Y/N)")
                    if 'y' in choice.lower():
                        tinh.delete()

        for huyen in Huyen.objects.all():
            if not is_vietnamese(huyen.name):
                if has_special_character(huyen.name):
                    huyen.delete()
                else:
                    choice = input(
                        f"Do you want to delete {huyen.name} ? (Y/N)")
                    if 'y' in choice.lower():
                        huyen.delete()

        for xa in Xa.objects.all():
            if not is_vietnamese(xa.name):
                if has_special_character(xa.name):
                    xa.delete()
                else:
                    choice = input(f"Do you want to delete {xa.name} ? (Y/N)")
                    if 'y' in choice.lower():
                        xa.delete()
