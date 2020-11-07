from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page

from app import huong_dan_tnv_views, thong_tin_views
from django.conf import settings
from app.admin import router
from app.index import IndexView
from app.ho_dan_views import HoDanListView

_common_cache = cache_page(
    settings.VIEW_CACHE_SETTINS['common'], key_prefix=settings.REVISION
)
_static_cache = cache_page(
    settings.VIEW_CACHE_SETTINS['static'], key_prefix=settings.REVISION
)

urlpatterns = [
    path('', _common_cache(IndexView.as_view()), name="index"),
    path('api/', include(router.urls)),
    # path('api/', rest_admin.site.urls, name="rest_api"),
    path('chaining/', include('smart_selects.urls')),
    path('admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),

    path('admin/', admin.site.urls, name="admin_home"),
    path('select2/', include('django_select2.urls')),

    re_path(
        r'^ho_dan/?$',
        _common_cache(HoDanListView.as_view()),
        name='home_ho_dan'
    ),
    path(
        'huong_dan_tnv/',
        _static_cache(huong_dan_tnv_views.index),
        name="home_huong_dan_tnv_url"
    ),
    path(
        'thong_tin/',
        _static_cache(thong_tin_views.index),
        name="home_thong_tin_url"),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
