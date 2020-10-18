import django
from django.contrib import admin
from django.db.models import Count, F
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.db import models
import datetime
from app.forms import UploadFileForm
from app.models import YoutubeClip, VIP, Publisher
from app.models import BadTopic, Policy, BadCase
from django.conf.locale.vi import formats as vi_formats
from django.forms import TextInput, Textarea
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter

vi_formats.DATETIME_FORMAT = "d/m/y H:i"

# admin interface

admin.site.site_header = 'Giám sát nội dung xấu độc trên Youtube'
admin.site.site_title = 'Giám sát nội dung xấu độc trên Youtube'
admin.index_title = 'Giám sát nội dung xấu độc trên Youtube'
admin.site_url = '/v1/app'


class BadTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_total_mention', 'count_mention_24h', 'count_mention_week')

    @mark_safe
    def count_total_mention(self, obj):
        count = obj.topic_videos.count()
        tag = f"<a href='/v1/app/youtubeclip/?topic__pk__exact={obj.pk}'> {count} đề cập </a>"
        return tag
    count_total_mention.short_description = "Tổng đề cập"
    count_total_mention.allow_tags = True 


    @mark_safe
    def count_mention_24h(self, obj):
        last_24h = django.utils.timezone.now() - datetime.timedelta(hours=24)
        count = obj.topic_videos.filter(publish_date__gt=last_24h).count()
        from_date = last_24h.strftime("%Y-%m-%d") 
        tag = f"<a href='/v1/app/youtubeclip/?topic__pk__exact={obj.pk}&publish_date__range__gte={from_date}'> {count} đề cập </a>"
        return tag
    count_mention_24h.short_description = "Đề cập 24h qua"
    count_mention_24h.allow_tags = True

    @mark_safe
    def count_mention_week(self, obj):
        last_week = django.utils.timezone.now() - datetime.timedelta(days=7)
        count = obj.topic_videos.filter(publish_date__gt=last_week).count()
        from_date = last_week.strftime("%Y-%m-%d") 
        tag = f"<a href='/v1/app/youtubeclip/?topic__pk__exact={obj.pk}&publish_date__range__gte={from_date}'> {count} đề cập </a>"
        return tag

    count_mention_week.short_description = "Đề cập 1 tuần qua"
    count_mention_week.allow_tags = True





class BadContentInline(admin.StackedInline):
    model = BadCase


# admin models 
class YoutubeClipAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'get_publisher', 'topic', 'get_url', 'get_mentions', 'live_status', 'bad_content_status', 'get_violation', 'get_content')
    list_filter = (('publish_date', DateRangeFilter), ('live_status', ChoiceDropdownFilter), ('bad_content_status', ChoiceDropdownFilter), ('mentions', RelatedDropdownFilter), ('publisher', RelatedDropdownFilter), ('topic', RelatedDropdownFilter))
    search_fields = ('title', 'content', 'publisher__name' )
    list_editable = ('live_status', 'bad_content_status')
    date_hierarchy = 'publish_date'
    inlines = [
        BadContentInline
    ]

    class Meta:
        order_by = '-publish_date'

    def get_form(self, request, obj=None, **kwargs):
        form = super(YoutubeClipAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['title'].widget.attrs['style'] = 'min-width: 400px;'
        return form


    def get_content(self, obj):
        if obj.content:
            return ' '.join(obj.content.split()[:10]) + '...'
        else:
            return ''
    get_content.short_description = "Bóc băng"

    def get_publish_date(self, obj):
        if not obj.publish_date:
            return ''
        else:
            return obj.publish_date.strftime( "%d/%m/%y")

    get_publish_date.short_description = "Xuất bản"

    @mark_safe
    def get_publisher(self, obj):
        tag = f'<a href="/v1/app/publisher/{obj.publisher.pk}/"> {obj.publisher.name} </a>'
        return tag
    get_publisher.short_description = "Chủ kênh"
    get_publisher.allow_tags = True
        

    @mark_safe
    def get_url(self, obj):
        return '<a href="%s">%s</a>' % (obj.url, obj.url)

    get_url.allow_tags = True
    get_url.short_description = "Link"


    @mark_safe
    def get_mentions(self, obj):
        mentions = {f"<a href='/v1/app/vip/{x.pk}/'>{x.name} ({x.code_name})</a>" for x in obj.mentions.all()}
        if mentions:
            return '; '.join(list(mentions))
        else:
            return ''
    get_url.allow_tags = True
    get_mentions.short_description = "Đề cập tới"

    
    def get_violation(self, obj):
        violations = {x.violate.name for x in obj.badcontent.all()}
        if violations:
            return '; '.join(list(violations))
        else:
            return ''
    
    get_violation.short_description = "Hành vi vi phạm"
        
class YoutubeClipInline(admin.StackedInline):
    model = YoutubeClip
    verbose_name = "Video"
    verbose_name_plural = "Videos"
    fields = ('title', 'url', 'publish_date', 'live_status', 'bad_content_status')
    extra = 0   

    # def get_queryset(self, request):
    #     LIMIT_SEARCH = 25
    #     queryset = super(YoutubeClipInline, self).get_queryset(request)
    #     ids = queryset.order_by('-publish_date').values('pk')[:LIMIT_SEARCH]
    #     ids = [x['pk'] for x in ids]
    #     qs = YoutubeClip.objects.filter(pk__in=ids).order_by('-publish_date')
    #     return qs

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('tracking', 'name', 'video_count', 'video_count_today', 'video_count_week', 'url')
    list_display_links = ('name', )
    search_fields = ('name', )
    list_editable = ('tracking', )
    ordering = ('video_count', 'video_count_today', 'video_count_week')
    inlines = (YoutubeClipInline, )

    class Meta:
        order_by = '-video_count_today'



class MentionInline(admin.StackedInline):
    model = VIP.mention_clips.through
    verbose_name = "Clip đề cập"
    verbose_name_plural = "Clip đề cập"
    extra = 0


class VIPAdmin(admin.ModelAdmin):
    list_display = ('code_name', 'name', 'position', 'count_total_mention', 'count_mention_24h', 'count_mention_week')
    search_fields = ('name', 'code_name')
    list_display_links = ('code_name', 'name')
    # inlines = [MentionInline]


    def get_queryset(self, request):
        """Sort by mention_clips"""
        return VIP.objects.annotate(count_clip=Count('mention_clips')).order_by('-count_clip')

    @mark_safe
    def count_total_mention(self, obj):
        count = obj.mention_clips.count()
        tag = f"<a href='/v1/app/youtubeclip/?mentions__id__exact={obj.pk}'> {count} đề cập </a>"
        return tag
    count_total_mention.short_description = "Tổng đề cập"
    count_total_mention.allow_tags = True 


    @mark_safe
    def count_mention_24h(self, obj):
        last_24h = django.utils.timezone.now() - datetime.timedelta(hours=24)
        count = obj.mention_clips.filter(publish_date__gt=last_24h).count()
        from_date = last_24h.strftime("%Y-%m-%d") 
        tag = f"<a href='/v1/app/youtubeclip/?mentions__id__exact={obj.pk}&publish_date__range__gte={from_date}'> {count} đề cập </a>"
        return tag
    count_mention_24h.short_description = "Đề cập 24h qua"
    count_mention_24h.allow_tags = True

    @mark_safe
    def count_mention_week(self, obj):
        last_week = django.utils.timezone.now() - datetime.timedelta(days=7)
        count = obj.mention_clips.filter(publish_date__gt=last_week).count()
        from_date = last_week.strftime("%Y-%m-%d") 
        tag = f"<a href='/v1/app/youtubeclip/?mentions__id__exact={obj.pk}&publish_date__range__gte={from_date}'> {count} đề cập </a>"
        return tag

    count_mention_week.short_description = "Đề cập 1 tuần qua"
    count_mention_week.allow_tags = True



class BadCaseAdmin(admin.ModelAdmin):
    list_display = ('sentence', 'get_youtube_clip', 'get_publisher', 'contain_bad_content', 'violate')
    list_editable = ('contain_bad_content', 'violate')
    list_filter = ('contain_bad_content', )

    @mark_safe
    def get_youtube_clip(self, obj):
        tag = f'<a href="{obj.youtube_clip.url}">{obj.youtube_clip.title}</a>'
        return tag
    
    get_youtube_clip.short_description = "Clip chứa nội dung"
    get_youtube_clip.allow_tags = True
    

    def get_publisher(self, obj):
        return obj.youtube_clip.publisher.name
    get_publisher.short_description = "Nguồn phát tán"


admin.site.register(Publisher, PublisherAdmin)
admin.site.register(BadCase, BadCaseAdmin)
admin.site.register(YoutubeClip, YoutubeClipAdmin)
admin.site.register(Policy)
admin.site.register(VIP, VIPAdmin)
admin.site.register(BadTopic, BadTopicAdmin)
