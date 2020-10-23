import datetime
import django
from django.core.management.base import BaseCommand
from app.models import Tinh, Huyen, Xa, Thon, HoDan


class Command(BaseCommand):
    def handle(self, **options):
        """Merge du lieu tinh, huyen, xa bi trung lap"""
        # tinhs = Tinh.objects.all()
        # for tinhA in tinhs:
        #     print(f"Kiem tra tinh {tinhA.name}")
        #     nameA = tinhA.name.strip().lower()
        #     for tinhB in tinhs:
        #         nameB = tinhB.name.strip().lower()
        #         if tinhA.pk != tinhB.pk and (nameB in nameA):  # duplicated
        #             print(
        #                 f"Phat hien {nameB} ({tinhB.pk}) trung lap voi {nameA}({tinhA})")
        #             # update ho dan cua B sang A
        #             HoDan.objects.filter(tinh=tinhB).update(tinh=tinhA)

        #             # remove tinhB
        #             # try:
        #             if True:
        #                 tinhB.delete()
        #             # except:
        #                 # pass

        # tinhs = Huyen.objects.all()
        # for tinhA in tinhs:
        #     try:
        #         print(f"Kiem tra huyen {tinhA.name}")
        #         nameA = tinhA.name.strip().lower()
        #         for tinhB in tinhs:
        #             nameB = tinhB.name.strip().lower()
        #             if tinhA.pk != tinhB.pk and (nameB in nameA):  # duplicated
        #                 print(
        #                     f"Phat hien {nameB} ({tinhB.pk}) trung lap voi {nameA}({tinhA})")
        #                 # update ho dan cua B sang A
        #                 HoDan.objects.filter(huyen=tinhB).update(huyen=tinhA)

        #                 # remove tinhB
        #                 tinhB.delete()
        #     except:
        #         pass

        tinhs = Xa.objects.all()
        for tinhA in tinhs:
            try:
                print(f"Kiem tra xa {tinhA.name}")
                nameA = tinhA.name.strip().lower()
                for tinhB in tinhs:
                    nameB = tinhB.name.strip().lower()
                    if tinhA.pk != tinhB.pk and (nameB in nameA):  # duplicated
                        print(
                            f"Phat hien {nameB} ({tinhB.pk}) trung lap voi {nameA}({tinhA})")
                        # update ho dan cua B sang A
                        HoDan.objects.filter(xa=tinhB).update(xa=tinhA)

                        # remove tinhB
                        tinhB.delete()
            except:
                pass

        # tinhs = Thon.objects.all()
        # for tinhA in tinhs:
        #     try:
        #         print(f"Kiem tra thon {tinhA.name}")
        #         nameA = tinhA.name.strip().lower()
        #         for tinhB in tinhs:
        #             nameB = tinhB.name.strip().lower()
        #             if tinhA.pk != tinhB.pk and (nameB in nameA):  # duplicated
        #                 print(
        #                     f"Phat hien {nameB} ({tinhB.pk}) trung lap voi {nameA}({tinhA})")
        #                 # update ho dan cua B sang A
        #                 HoDan.objects.filter(thon=tinhB).update(thon=tinhA)

        #                 # remove tinhB
        #                 tinhB.delete()
        #     except:
        #         pass
