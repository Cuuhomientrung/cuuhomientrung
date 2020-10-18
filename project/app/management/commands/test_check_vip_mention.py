from app.business import check_VIP_mention
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, **options):
        """Test get videos from a channel"""
        check_VIP_mention()

