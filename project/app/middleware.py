from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.middleware import MiddlewareMixin
from django.urls import resolve
from django.middleware.csrf import CsrfViewMiddleware


class AutomaticUserLoginMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        # NOTE: Following code is to bypass login page. Change username to default login user you want
        user = User.objects.get(username='user1')
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
