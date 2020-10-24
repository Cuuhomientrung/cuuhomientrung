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
from django_restful_admin import admin as rest_admin
from app import ho_dan_views
from app.index import index

urlpatterns = [
    path('',index,name="index"),
    path('admin/', admin.site.urls, name="admin_home"),
    # path('api/', rest_admin.site.urls, name="rest_api"),
    path('chaining/', include('smart_selects.urls')),
    url(r'^admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),
    path('select2/', include('django_select2.urls')),
    url(r'^ho_dan$', ho_dan_views.index),
]
