from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.middleware import MiddlewareMixin
from django.http import HttpResponseForbidden


class AutomaticUserLoginMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):

        # NOTE: Following code is to bypass login page. Change username to default login user you want 
        user = User.objects.get(username='user1')
        request.user = user
        auth.login(request, user)
#
