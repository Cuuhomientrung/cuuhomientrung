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
from django.urls import path, re_path, include
from rest_framework import routers
# from django_restful_admin import admin as api_admin 
from app.views import CheckYoutubeLinkView
# router = routers.DefaultRouter()
# router.register(r'tasks', TaskViewSet, "task")

urlpatterns = [
    # path('v1/app/', CheckYoutubeLinkView.as_view()),
    path('', CheckYoutubeLinkView.as_view()),
    path('v1/', admin.site.urls),
    # path('', admin_site.urls),
    # re_path(r'^v1/api-auth/', include('rest_framework.urls'))
]