from app.business import check_youtube_live_status
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, **options):
        """Test get videos from a topic search"""
        check_youtube_live_status()

