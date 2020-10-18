from app.business import get_publisher_videos, track_publisher
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, **options):
        """Test get videos from a channel"""
        result = track_publisher(max_publisher=10, min_duration=60)

