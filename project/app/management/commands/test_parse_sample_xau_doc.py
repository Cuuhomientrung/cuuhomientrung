from app.business import download_youtube_mp3, parse_audio_to_text
from app.models import YoutubeClip
from django.core.management.base import BaseCommand
from django.conf import settings
import random

class Command(BaseCommand):
    def handle(self, **options):
        """Parse xau doc video to sentences for training AI"""
        number = 3
        bad_clips = random.choices(YoutubeClip.objects.filter(use_as_example=True, parse_sentence_for_training=False).all(), k=number)

        for clip in bad_clips:
            if clip.bad_content_status <=1:
                download_youtube_mp3(clip)
                if parse_audio_to_text(clip):
                    clip.parse_content_to_label()
                    clip.parse_sentence_for_training = True
                    clip.save()
            else:
                clip.parse_content_to_label()
                clip.parse_sentence_for_training = True
                clip.save()


            



