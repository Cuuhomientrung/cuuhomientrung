from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.generic.edit import FormView
from app.business import check_youtube_link
from app.forms import UploadFileForm
from django.shortcuts import render, redirect 
from app.models import YoutubeClip
from django.contrib.admin.views.decorators import staff_member_required

from datetime import datetime
# from app.models import Task, RenderServer
# from app.serializer import TaskSerializer, RenderServerSerializer

class CheckYoutubeLinkView(FormView):
    template_name = 'admin/index.html'
    form_class = UploadFileForm
    success_url = 'v1/app/item/'

    def form_valid(self, form):
        url_list = form.get_url_list()
        if url_list:
            for item in url_list:
                print(item)
                stt = str(item[0])
                group = str(item[1])
                classify = str(item[2])
                url = str(item[3])
                views = str(item[4])

                publish_date = datetime.strptime(str(item[5]), "%m/%d/%y")
                send_date = datetime.strptime(str(item[6]), "%m/%d/%y")
                content_type = str(item[7])
                
                new_item, _created = YoutubeClip.objects.get_or_create(
                    url = url
                )
                if _created:
                    new_item.stt = stt
                    new_item.group = group
                    new_item.classify = classify
                    new_item.views = views 
                    new_item.publish_date = publish_date
                    new_item.send_date = send_date
                    new_item.content_type = content_type
                    new_item.save()

                if new_item.status == 5 or new_item.status == 3: # only recheck health if result hasn't been set or link is alive
                    if 'youtube' in new_item.url:
                        check_youtube_link.delay(new_item.pk) # async call to check link status 

        return redirect("v1/app/item/")