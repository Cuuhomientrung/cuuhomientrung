from django.core.management.base import BaseCommand
from django.conf import settings

from app.models import YoutubeClip
from app.business import download_youtube_mp3, parse_audio_to_text
import random


class Command(BaseCommand):
    def handle(self, **options):
        """Start scheduling task to make video clip"""
        item = random.choice(YoutubeClip.objects.filter(bad_content_status=0).all())
        download_youtube_mp3(item)