from app.models import Publisher, YoutubeClip, VIP
from app.lib.utils import open_utf8_file_to_read
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, **options):
        """Import bad youtube video link as sample label to train AI"""

        filename= 'bad_youtube_video_list_7.csv'
        full_path = settings.BASE_DIR + '/test/' + filename 

        with open_utf8_file_to_read(full_path) as stream:
            reader = csv.reader(stream, dialect='excel')
            count = 0
            for line in reader:
                if len(line) <= 1: # header / footer line 
                    continue

                count += 1
                print(f'Processing line {count}')
                print(f'Line content: {line}')
                publisher_name = str(line[0])
                publisher_url = str(line[1])
                video_url = str(line[2])

                if not video_url.strip(): # blank line 
                    continue

                video_title = str(line[3])
                try:
                    video_views = int(str(line[4]).replace(",", ''))
                except:
                    print(f"Can't parse views field: {str(line[4])}")
                    video_views = 0
                try:
                    video_published_date = datetime.strptime(str(line[5]), "%d/%m/%y")
                except:
                    print(f"Can't parse published date field: {str(line[5])}")
                    video_published_date = datetime.strptime(str(line[5]), "%m/%d/%y")

                publisher, created = Publisher.objects.get_or_create(
                    url = publisher_url
                )
                if created:
                    publisher.name = publisher_name
                    publisher.video_count = 1
                else:
                    publisher.video_count += 1

                publisher.save()

                video = YoutubeClip.objects.get_or_create(
                    title = video_title,
                    url = video_url,
                    views = video_views,
                    publish_date = video_published_date,
                    publisher = publisher,
                )