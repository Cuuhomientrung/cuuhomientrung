import string

from factory import fuzzy, SubFactory, Sequence
from factory.django import DjangoModelFactory

from .. import models

__all__ = [
    "HuyenFactory",
    "XaFactory",
    "ThonFactory",
    "TNVFactory",
    "CuuHoFactory",
    "HoDanFactory",
    "NguonLucFactory",
    "TinTucFactory"
]


class HuyenFactory(DjangoModelFactory):
    class Meta:
        model = models.Huyen

    name = Sequence(lambda n: "Huyện {}".format(n))
    tinh = fuzzy.FuzzyChoice(choices=models.Tinh.objects.all())


class XaFactory(DjangoModelFactory):
    class Meta:
        model = models.Xa

    name = Sequence(lambda n: "Xã {}".format(n))
    huyen = SubFactory(HuyenFactory)


class ThonFactory(DjangoModelFactory):
    class Meta:
        model = models.Thon

    name = Sequence(lambda n: "Thôn {}".format(n))
    huyen = SubFactory(HuyenFactory)


def get_status_choices(choices):
    return [status[0] for status in choices]


class TNVFactory(DjangoModelFactory):
    class Meta:
        model = models.TinhNguyenVien

    name = fuzzy.FuzzyText(prefix="TNV ")
    status = fuzzy.FuzzyChoice(choices=get_status_choices(models.TINHNGUYEN_STATUS))
    location = fuzzy.FuzzyText(prefix="Địa Chỉ ")
    phone = fuzzy.FuzzyText(chars=string.digits)
    note = fuzzy.FuzzyText(prefix="Ghi Chú ", length=100)
    tinh = fuzzy.FuzzyChoice(choices=models.Tinh.objects.all())
    huyen = SubFactory(HuyenFactory)
    xa = SubFactory(XaFactory)
    thon = SubFactory(ThonFactory)


class CuuHoFactory(DjangoModelFactory):
    class Meta:
        model = models.CuuHo

    name = fuzzy.FuzzyText(prefix="Đội cứu hộ ")
    status = fuzzy.FuzzyChoice(choices=get_status_choices(models.CUUHO_STATUS))
    tinh = fuzzy.FuzzyChoice(choices=models.Tinh.objects.all())
    location = fuzzy.FuzzyText(prefix="Phạm vi cứu hộ ")
    phone = fuzzy.FuzzyText(chars=string.digits)
    note = fuzzy.FuzzyText(prefix="Ghi Chú ", length=100)
    volunteer = SubFactory(TNVFactory)


class HoDanFactory(DjangoModelFactory):
    class Meta:
        model = models.HoDan

    name = fuzzy.FuzzyText(prefix="Hộ dân ")
    location = fuzzy.FuzzyText(prefix="Địa Chỉ ")
    status = fuzzy.FuzzyChoice(choices=models.TrangThaiHoDan.objects.all())
    people_number = fuzzy.FuzzyInteger(low=1)
    tinh = fuzzy.FuzzyChoice(choices=models.Tinh.objects.all())
    phone = fuzzy.FuzzyText(chars=string.digits)
    volunteer = SubFactory(TNVFactory)
    note = fuzzy.FuzzyText(prefix="Ghi Chú ", length=100)
    cuuho = SubFactory(CuuHoFactory)


class NguonLucFactory(DjangoModelFactory):
    class Meta:
        model = models.NguonLuc

    name = fuzzy.FuzzyText(prefix="Nguồn lực ")
    location = fuzzy.FuzzyText(prefix="Địa Chỉ ")
    status = fuzzy.FuzzyChoice(choices=get_status_choices(models.RESOURCE_STATUS))
    tinh = fuzzy.FuzzyChoice(choices=models.Tinh.objects.all())
    volunteer = SubFactory(TNVFactory)


class TinTucFactory(DjangoModelFactory):
    class Meta:
        model = models.TinTuc

    title = fuzzy.FuzzyText(prefix="Tin ", length=20)
    note = fuzzy.FuzzyText(prefix="Ghi Chú ", length=100)
