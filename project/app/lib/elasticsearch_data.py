import copy
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import *
from elasticsearch_dsl.query import MoreLikeThis
from elasticsearch_dsl.connections import connections
import os

# HOST = os.environ['DOCBAO_ELASTICSEARCH_HOST']
HOST = '127.0.0.1'

class Elastic_Article(Document):
    sentence = Text()
    pk       = Text()

    class Index:
        name="youtube_bad_content"
        settings = {
			"number_of_shards": 1,
        }


    def save(self, **kwargs):
        return super(Elastic_Article, self).save(**kwargs)


class ElasticSearch_Client:
# This class handle converting normal Article to ElasticSearch Article
	def __init__(self):
		# Create connection to Elasticsearch
		connections.create_connection( hosts=[HOST], timeout=20)
		# Check if index articles existed
		index = Index("youtube_bad_content")
		if not index.exists():
			Elastic_Article.init() # create new index

	def push_data(self, pk, sentence):
		# push article to Elasticsearch
		elastic_article = Elastic_Article()
		elastic_article.sentence = sentence # convert article to elastic_article
		elastic_article.pk = str(pk)
		elastic_article.save()

	def get_similar_sentence(self, sentence):
		search = Search().using(Elasticsearch(HOST))
		result = search.query(MoreLikeThis(like=sentence, fields=['sentence'])).execute().to_dict()
		total = result['hits']['total']['value']
		max_score = result['hits']['max_score']
		if total > 0 and max_score > 0.5:
			first_hit = result['hits']['hits'][0]['pk']
			sentence = result['hits']['hits'][0]['sentence']
			return first_hit, sentence
		else:
			return None, None


