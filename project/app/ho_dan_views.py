from django.http import JsonResponse
from django.views.generic import ListView
from django.db.models import Q

from .models import HoDan, Tinh, Huyen, Xa, TrangThaiHoDan


class HoDanListView(ListView):
    model = HoDan
    paginate_by = 20
    template_name = "ho_dan_index.html"

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            # For search query params
            tinh = request.GET.get("tinh")
            huyen = request.GET.get("huyen")

            if tinh and int(tinh) > 0:
                list_huyen = self._get_huyen_xa_filtered(
                    Huyen, accept_empty=False
                ).values("id", "name")
                dict_huyen = {huyen["id"]: huyen["name"] for huyen in list_huyen}
                return JsonResponse(dict_huyen)

            if huyen and int(huyen) > 0:
                list_xa = self._get_huyen_xa_filtered(Xa, accept_empty=False).values(
                    "id", "name"
                )
                dict_xa = {xa["id"]: xa["name"] for xa in list_xa}
                return JsonResponse(dict_xa)

            return JsonResponse({})

        return super(HoDanListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        query_parms = self._get_query_params(self.request)
        query_parms.pop("page_number")
        query_condition = Q()
        qs = super(HoDanListView, self).get_queryset()

        for key, val in query_parms.items():
            if val:
                query_condition.add(Q(**{key: val}), Q.AND)

        qs = (
            qs.filter(query_condition).prefetch_related().order_by("-update_time", "id")
        )
        fields = []
        for _, field in enumerate(self.model._meta.get_fields()):
            name = field.name
            if field.many_to_one:
                id_field = name + "_id"
                name = name + "__name"
                fields.append(id_field)
            fields.append(name)

        return qs.values(*fields)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_status"] = TrangThaiHoDan.objects.all()
        context["ho_dan_total_count"] = self.get_queryset().count()
        context["list_tinh"] = Tinh.objects.select_related().order_by("name").all()
        context["list_huyen"] = self._get_huyen_xa_filtered(Huyen)
        context["list_xa"] = self._get_huyen_xa_filtered(Xa)
        params = self._get_query_params(self.request)
        params.pop("page_number")

        context["params_url"] = self._build_params_url(**params)
        context["filtered"] = params
        context["emergency_ids"] = [3, 5, 6]
        return context

    def _get_huyen_xa_filtered(self, model, accept_empty=True):
        qs = model.objects.order_by("name")
        tinh = self.request.GET.get("tinh", 0)
        huyen = self.request.GET.get("huyen", 0)

        tinh_id = int(tinh) if tinh and int(tinh) > 0 else None
        huyen_id = int(huyen) if huyen and int(huyen) > 0 else None

        if model.__name__ == "Huyen" and tinh_id:
            return qs.prefetch_related("tinh").filter(tinh_id=tinh_id)

        if model.__name__ == "Xa" and huyen_id:
            return qs.prefetch_related("huyen").filter(huyen_id=huyen_id)

        if not accept_empty:
            return qs
        return []

    @staticmethod
    def _get_query_params(request):
        return {
            "status": request.GET.get("status"),
            "tinh": request.GET.get("tinh"),
            "huyen": request.GET.get("huyen"),
            "xa": request.GET.get("xa"),
            "page_number": request.GET.get("page"),
        }

    @staticmethod
    def _build_params_url(status=None, tinh=None, huyen=None, xa=None):
        url = "?"
        if status:
            url = url + "status=" + status + "&"
        if tinh:
            url = url + "tinh=" + tinh + "&"
        if huyen:
            url = url + "huyen=" + huyen + "&"
        if xa:
            url = url + "xa=" + xa + "&"
        return url
