from app.models import Publisher
import csv
from app.lib.utils import open_utf8_file_to_read
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, **options):
        """Import VIP list into system"""
        filename= 'publisher_list.csv'
        full_path = settings.BASE_DIR + '/test/' + filename 

        with open_utf8_file_to_read(full_path) as stream:
            reader = csv.reader(stream, dialect='excel')
            for line in reader:
                name = str(line[0])
                count = str(line[1])
                url = str(line[2])

                publisher, created = Publisher.objects.get_or_create(
                    name = name,
                    video_count = count,
                    url = url
                )