from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.middleware import MiddlewareMixin
from django.http import HttpResponseForbidden


class AutomaticUserLoginMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        # if not AutomaticUserLoginMiddleware._is_user_authenticated(request):
        #     user = auth.authenticate(request)
        #     if user is None: #         return HttpResponseForbidden() # user = User.objects.get(username='user1')
        # user = User.objects.get(username='admin')
        user = User.objects.get(username='user1')
        request.user = user
        auth.login(request, user)
# 