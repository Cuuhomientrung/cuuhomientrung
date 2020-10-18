from app.business import parse_youtube_clip_to_text
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, **options):
        """Test get videos from a channel"""
        parse_youtube_clip_to_text(max_clip=2)

