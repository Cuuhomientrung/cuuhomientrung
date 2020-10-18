from app.lib.elasticsearch_data import ElasticSearch_Client
from app.models import BadCase
from django.core.management.base import BaseCommand
from django.conf import settings
import random

class Command(BaseCommand):
    def handle(self, **options):
        """Push all bad sample to elasticsearch"""
        es = ElasticSearch_Client()
        for case in BadCase.objects.filter(contain_bad_content=True, push_to_elasticsearch=False):
            es.push_data(case.pk, case.sentence)


            



