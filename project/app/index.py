import datetime
import pytz

from django.db.models import Count
from django.urls import reverse
from django.views.generic import TemplateView

from .settings import TIME_ZONE
from .admin import TinhAdmin
from .models import HoDan, CuuHo, TinhNguyenVien


class IndexView(TemplateView):
    template_name = "home_index.html"
    compare_time = datetime.datetime(
        2020, 10, 26, 17, 0, 0, tzinfo=datetime.timezone.utc
    ).astimezone(tz=pytz.timezone(TIME_ZONE))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tong_hodan_da_duoc_cuu"] = HoDan.objects.filter(status_id=7).count()
        context["tong_hodan_cap_cuu"] = HoDan.objects.filter(status_id=3).count()
        context["tong_doi_cuu_ho_san_sang"] = CuuHo.objects.filter(status=1).count()
        context["tong_tinh_nguyen_vien"] = TinhNguyenVien.objects.count()
        context["tinh_infos"] = self._get_tinh_info()
        return context

    def _get_tinh_info(self, limit=10):
        hodan_da_cuu = self._get_ho_dan_da_cuu_by_tinh()
        cuuho_by_tinh = self._get_cuu_ho_by_tinh()
        hodan_can_cuu = self._get_ho_dan_can_cuu_by_tinh()
        hodan_url = reverse("home_ho_dan")
        tinh_infos = []

        # tìm list dài nhất để là target để loop,
        # 2 list còn lại dùng để so sánh vả update phần tử
        _list = [hodan_da_cuu, hodan_can_cuu, cuuho_by_tinh]
        _list_len = [
            len(hodan_da_cuu),
            len(hodan_can_cuu),
            len(cuuho_by_tinh),
        ]  # same order as _list

        longest = max(_list_len)
        index = _list_len.index(longest)

        # index của max trong _list_len cũng chính là
        # index của list dài nhất trong _list
        target_list = _list[index]
        _list.remove(target_list)

        # Vì độ dài của các list ko bằng nhau,
        # nên chọn list dài nhất để loop để không bị thiếu
        for ind, val in enumerate(target_list):
            info = {
                "url": f'{hodan_url}?{TinhAdmin.URL_CUSTOM_TAG}={val["tinh_id"]}',
                "can_cuu_count": 0,
                "da_cuu_count": 0,
                "cuu_ho_count": 0
            }
            info.update(val)

            # Lấy dict có id tương ứng ở list thứ nhất
            info1 = self._get_list_element_by_value(_list[0], val["tinh_id"])
            if info1:
                # remove dict này khỏi list để lượt loop tiếp theo ko bị trùng
                _list[0].remove(info1)
                info.update(info1)

            # lấy dict có id tương ứng ở list thứ hai
            info2 = self._get_list_element_by_value(_list[1], val["tinh_id"])
            if info2:
                # remove dict này khỏi list để lượt loop tiếp theo ko bị trùng
                _list[1].remove(info2)
                info.update(info2)

            tinh_infos.append(info)

        # Limit results
        return tinh_infos[:limit]

    @staticmethod
    def _get_list_element_by_value(_list, tinh_id):
        for _, val in enumerate(_list):
            if val.get("tinh_id") == tinh_id:
                return val
        return None

    def _get_ho_dan_can_cuu_by_tinh(self):
        """
        Lấy tất cả Hộ Dân cần cứu rồi group lại theo tỉnh.
        Return:
            list of dict: Sort theo id của tỉnh
            [
                {
                    "tinh__name": Quảng Bình,
                    "tinh_id": 1,
                    "can_cuu_count": 10
                },
                {
                    "tinh__name": Quảng Bình,
                    "tinh_id": 2,
                    "can_cuu_count": 10
                },
                ...
            ]
        """
        ho_dan_can_cuu_by_tinh = (
            HoDan.objects.filter(created_time__gt=self.compare_time)
            .exclude(status_id=7)
            .values("tinh__name", "tinh_id")
            .annotate(can_cuu_count=Count("tinh"))
        )
        ho_dan_can_cuu_by_tinh = [i for i in ho_dan_can_cuu_by_tinh if i["tinh_id"]]
        sorted_can_cuu_by_tinh = sorted(
            ho_dan_can_cuu_by_tinh, key=lambda i: i["tinh_id"]
        )

        return sorted_can_cuu_by_tinh

    def _get_ho_dan_da_cuu_by_tinh(self):
        """
        Lấy tất cả Hộ Dân đã cứu rồi group lại theo tỉnh.
        Return:
            list of dict: Sort theo id của tỉnh
            [
                {
                    "tinh__name": Quảng Bình,
                    "tinh_id": 1,
                    "da_cuu_count": đã10
                },
                {
                    "tinh__name": Quảng Bình,
                    "tinh_id": 2,
                    "da_cuu_count": 10
                },
                ...
            ]
        """
        ho_dan_da_cuu_by_tinh = (
            HoDan.objects.filter(created_time__gt=self.compare_time, status_id=7)
            .values("tinh__name", "tinh_id")
            .annotate(da_cuu_count=Count("tinh"))
        )

        ho_dan_da_cuu_by_tinh = [i for i in ho_dan_da_cuu_by_tinh if i["tinh_id"]]
        sorted_da_cuu_by_tinh = sorted(
            ho_dan_da_cuu_by_tinh, key=lambda i: i["tinh_id"]
        )

        return sorted_da_cuu_by_tinh

    def _get_cuu_ho_by_tinh(self):
        """
        Lấy danh sách tất cả Cứu Hộ rồi group lại theo tỉnh.
        Return:
            list of dict: Sort theo id của tỉnh
            [
                {
                    "tinh__name": Quảng Bình,
                    "tinh_id": 1,
                    "cuu_ho_count": 10
                },
                {
                    "tinh__name": Quảng Bình,
                    "tinh_id": 2,
                    "cuu_ho_count": 10
                },
                ...
            ]
        """
        cuu_ho_tinh = CuuHo.objects.values("tinh__name", "tinh_id").annotate(
            cuu_ho_count=Count("tinh")
        )
        cuu_ho_tinh = [i for i in cuu_ho_tinh if i["tinh_id"]]
        sorted_cuu_ho_by_tinh = sorted(cuu_ho_tinh, key=lambda i: i["tinh_id"])
        return sorted_cuu_ho_by_tinh
