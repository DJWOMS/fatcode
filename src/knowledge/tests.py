from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from src.knowledge.models import Article, Category, Tag


class ArticleTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_article(self):
        request = self.client.get('/api/v1/knowledge/article/')
