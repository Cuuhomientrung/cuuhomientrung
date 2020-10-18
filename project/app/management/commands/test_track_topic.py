from app.business import get_publisher_videos, track_publisher, track_topic
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, **options):
        """Test get videos from a topic search"""
        result = track_topic(max_topic=10, min_duration=60)

