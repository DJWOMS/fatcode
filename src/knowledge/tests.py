from collections import OrderedDict

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from src.knowledge import models
from src.profiles.models import FatUser


class TestKnowledge(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user = FatUser.objects.create(
            username='anton',
            password='V97tn7M4rU',
            email='anton@example.com'
        )
        models.Article.objects.create(
            title='first article',
            text='text of the first article',
            author=user,
            published=True,
        )
        models.Article.objects.create(
            title='second article',
            text='text of the second article',
            author=user,
            published=True,
        )

        models.Tag.objects.create(name='python')
        models.Tag.objects.create(name='django')

        models.Glossary.objects.create(letter="f")

        models.Category.objects.create(name='Python')
        web_cat = models.Category.objects.create(name='Web')
        models.Category.objects.create(name='Django', parent=web_cat)

    def test_article_list(self):
        request = self.client.get(reverse("article-list"))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data["results"]), 2)

    def test_article_detail(self):
        article = models.Article.objects.get(title='first article')
        request = self.client.get(reverse("article-detail", kwargs={"pk": article.pk}))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['title'], 'first article')
        self.assertEqual(request.data['text'], 'text of the first article')

    def test_tag_list(self):
        request = self.client.get(reverse("tag-list"))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.json().get('results')), 2)

    def test_category_list(self):
        request = self.client.get(reverse("category-list"))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.json().get('results')), 3)

    def test_get_glossary_letters(self):
        request = self.client.get(reverse("glossary-letter"))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.json().get('results'), [{'id': 1, 'letter': 'f'}])


class CommentLikeTest(APITestCase):
    def setUp(self):
        self.profile1 = FatUser.objects.create(
            username='username1',
            email='test1@mail.ru',
            password='test1'
        )
        self.profile1.save()
        self.profile1_token = Token.objects.create(user=self.profile1)

        self.profile2 = FatUser.objects.create(
            username='username2',
            email='test2@mail.ru',
            password='test2'
        )
        self.profile2.save()
        self.profile2_token = Token.objects.create(user=self.profile2)

        self.profile3 = FatUser.objects.create(
            username='username4',
            email='test4@mail.ru',
            password='test4'
        )
        self.profile3.save()

        self.category1 = models.Category.objects.create(
            name='categoty1'
        )
        self.article1 = models.Article.objects.create(
            title='test',
            text='article1',
            author=self.profile1,
        )
        self.article1.category.add(self.category1)
        self.comment1 = models.CommentArticle.objects.create(
            text='test1',
            user=self.profile1,
            article=self.article1,
        )
        self.like1 = models.LikeDislike.objects.create(
            user=self.profile1,
            article=self.article1,
            status='Like'
        )

    def test_comment_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('article_comment', kwargs={'pk': self.article1.id}))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_comment_list_no_authorization(self):
        response = self.client.get(reverse('article_comment', kwargs={'pk': self.article1.id}))
        self.assertEqual(response.status_code, 401)

    def test_comment_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('comment_detail',
                                           kwargs={'pk': self.article1.id, 'comment_pk': self.comment1.id})
                                   )
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_comment_detail_no_authorization(self):
        response = self.client.get(reverse('comment_detail',
                                           kwargs={'pk': self.article1.id, 'comment_pk': self.comment1.id})
                                   )
        self.assertEqual(response.status_code, 401)

    def test_comment_create(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'text': 'test1',
            'user': self.profile1.id,
            'article': self.article1.id
        }
        response = self.client.post(reverse('article_comment', kwargs={'pk': self.article1.id}), data=data, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 201)

    def test_comment_create_no_authorization(self):
        data = {
            'text': 'test1',
            'user': self.profile3.id,
            'article': self.article1.id
        }
        response = self.client.post(reverse('article_comment', kwargs={'pk': self.article1.id}), data=data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_comment_author_update(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'text': 'test',
            'user': self.profile1.id,
            'article': self.article1.id
        }
        response = self.client.put(reverse('comment_detail',
                                           kwargs={'pk': self.article1.id, 'comment_pk': self.comment1.id}),
                                   data=data, format='json'
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_comment_update_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'text': 'test',
            'user': self.profile2.id,
            'article': self.article1.id
        }
        response = self.client.put(reverse('comment_detail',
                                           kwargs={'pk': self.article1.id, 'comment_pk': self.comment1.id}),
                                   data=data, format='json'
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_comment_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.delete(reverse('comment_detail',
                                           kwargs={'pk': self.article1.id, 'comment_pk': self.comment1.id})
                                   )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.CommentArticle.objects.filter(id=self.comment1.id).exists(), False)

    def test_comment_delete_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.delete(reverse('comment_detail',
                                           kwargs={'pk': self.article1.id, 'comment_pk': self.comment1.id})
                                   )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(models.CommentArticle.objects.filter(id=self.comment1.id).exists(), True)

    def test_like_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('article_like', kwargs={'pk': self.article1.id}))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_like_list_no_authorization(self):
        response = self.client.get(reverse('article_like', kwargs={'pk': self.article1.id}))
        self.assertEqual(response.status_code, 401)

    def test_like_create(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'user': self.profile2.id,
            'article': self.article1.id,
            'status': 'Like'
        }
        response = self.client.post(reverse('article_like', kwargs={'pk': self.article1.id}), data=data, format='json')
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, 201)

    def test_like_create_prohibit(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'user': self.profile1.id,
            'article': self.article1.id,
            'status': 'Like'
        }
        response = self.client.post(reverse('article_like', kwargs={'pk': self.article1.id}), data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_like_create_no_authorization(self):
        data = {
            'user': self.profile3.id,
            'article': self.article1.id,
            'status': 'Like'
        }
        response = self.client.post(reverse('article_like', kwargs={'pk': self.article1.id}), data=data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_likeauthor_update(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'user': self.profile1.id,
            'article': self.article1.id,
            'status': 'Dislike'
        }
        response = self.client.put(reverse('like_update',
                                           kwargs={'pk': self.article1.id, 'like_pk': self.like1.id}),
                                   data=data, format='json'
                                   )
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, 200)

    def test_like_update_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'user': self.profile2.id,
            'article': self.article1.id,
            'status': 'Dislike'
        }
        response = self.client.put(reverse('like_update',
                                           kwargs={'pk': self.article1.id, 'like_pk': self.like1.id}),
                                   data=data, format='json'
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

