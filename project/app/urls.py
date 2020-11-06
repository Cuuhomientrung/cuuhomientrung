"""docbao_crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from app import ho_dan_views, huong_dan_tnv_views, thong_tin_views
from django.conf import settings
from app.admin import router
from app.index import IndexView
from django.views.decorators.cache import cache_page

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
    url(r'^admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),

    path('admin/', admin.site.urls, name="admin_home"),
    path('select2/', include('django_select2.urls')),

    url(
        r'^ho_dan$',
        _common_cache(ho_dan_views.index),
        name='home_ho_dan'
    ),
    url(
        r'^get_huyen_api/?$',
        _common_cache(ho_dan_views.get_huyen_api)
    ),
    url(
        r'^get_xa_api/?$',
        _common_cache(ho_dan_views.get_xa_api)
    ),
    url(
        'huong_dan_tnv/',
        _static_cache(huong_dan_tnv_views.index),
        name="home_huong_dan_tnv_url"
    ),
    url(
        'thong_tin/',
        _static_cache(thong_tin_views.index),
        name="home_thong_tin_url"),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
