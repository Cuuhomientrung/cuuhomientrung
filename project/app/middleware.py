from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.middleware import MiddlewareMixin
from django.urls import resolve
from django.middleware.csrf import CsrfViewMiddleware
from django.shortcuts import redirect


class CustomCacheMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        response = self.get_response(request)

        app_name = resolve(request.path_info).app_name
        if app_name == 'django_select2':
            response["Cache-Control"] = "max-age=0, no-cache, no-store, must-revalidate, private"

        return response


class AutomaticUserLoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.GET.get('adminr', None):
            auth.logout(request)
            return redirect('/admin/login/?r=1')

        if not request.path == '/admin/login/' and\
                not request.user.is_authenticated and\
                not request.GET.get('r', None):
            # NOTE: Following code is to bypass login page. Change username to default login user you want
            user = User.objects.get(username='user1')
            # user = User.objects.get(username='admin')
            request.user = user
            auth.login(request, user)


class RestAPICsrfMiddleware(CsrfViewMiddleware):

    def process_view(self, request, callback, callback_args, callback_kwargs):
        """Django restful admin -> skip csrf check.
        """

        app_name = resolve(request.path_info).app_name
        if app_name == 'django_restful_admin':
            return self._accept(request)
        else:
            # Origin csrf token check for other routes
            return super(RestAPICsrfMiddleware, self).process_view(
                request, callback, callback_args, callback_kwargs
            )
