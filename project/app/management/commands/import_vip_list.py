from app.models import YoutubeClip, VIP
from app.business import download_youtube_mp3, parse_audio_to_text, check_bad_content
import csv
from app.lib.utils import open_utf8_file_to_read
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, **options):
        """Import VIP list into system"""
        filename= 'vip_list.csv'
        full_path = settings.BASE_DIR + '/test/' + filename 

        with open_utf8_file_to_read(full_path) as stream:
            reader = csv.reader(stream, dialect='excel')
            for line in reader:
                code_name = str(line[0])
                name = str(line[1])
                position = str(line[2])
                main_keyword = str(line[3]).replace(',', ';')
                combine_keyword = str(line[4]).replace(',', ';')
                exclude_keyword = str(line[5]).replace(',', ';')

                vip, created = VIP.objects.get_or_create(
                    code_name = code_name,
                    name = name,
                    position = position,
                    main_keyword = main_keyword,
                    combine_keyword = combine_keyword,
                    exclude_keyword = exclude_keyword
                )