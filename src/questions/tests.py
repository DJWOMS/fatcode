from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from src.profiles.models import FatUser

from .models import Question, QuestionReview, Answer
from . import serializers


class QuestionApiViewTestCase(APITestCase):

    def create_answerObject(self):
        answer = Answer.objects.create(
            question=self.question,
            text='123',
            author=self.user
        )
        return answer

    def setUp(self):
        self.user = FatUser.objects.create_user(
            username='user',
            password='password',
            email='emailunique@mail.ru'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.question = Question.objects.create(title='title1', author=self.user, text='text')

    def test_create_question(self):
        data = {
            "title": "boobs",
            "text": "big boobs",
            "tags": [
                {
                    "boob"
                }
            ]
        }
        response = self.client.post(reverse("questions"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_question_list(self):
        response = self.client.get(reverse("questions"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_answer(self):
        data = {
            'question': self.question.id,
            'text': 'text_for_answer'
        }
        response = self.client.post(reverse("create-answer"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_detail_question(self):
        url = reverse("question", kwargs={"pk": self.question.id})
        response = self.client.get(url)
        serialize = serializers.RetrieveQuestionSerializer(self.question)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("text"), serialize.data.get("text"))

    def test_update_question(self):
        data = {
            "title": "title2",
            "text": "text2",
            "tags": [
                {
                  "name": "name2"
                }
            ]
        }
        url = reverse("question", kwargs={"pk": self.question.id})
        response = self.client.patch(url, data, format='json')
        self.question = Question.objects.get(id=self.question.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.question.text, data['text'])

    def test_update_answer(self):
        data = {
            'text': 'updated_text'
        }
        answer = self.create_answerObject()
        url = reverse("answer", kwargs={"pk": answer.id})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_answer(self):
        answer = self.create_answerObject()
        url = reverse("answer", kwargs={"pk": answer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Answer.objects.exists(), False)

    def test_delete_question(self):
        url = reverse("question", kwargs={"pk": self.question.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.exists(), False)

    def test_question_review(self):
        data = {
            'grade': 'false',
            'question': self.question.id,
        }
        url = reverse("question-review")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_repeat_question_review(self):
        QuestionReview.objects.create(
            question=self.question,
            user=self.user,
            grade=False
        )
        data = {
            'grade': False,
            'question': self.question.id,
        }
        url = reverse("question-review")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_review(self):
        answer = self.create_answerObject()
        data = {
            'grade': False,
            'answer': f'{answer.id}',
        }
        url = reverse("answer-review")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_is_not_author(self):
        user = FatUser.objects.create_user(
            username='user2',
            password='password2',
            email='123123email@mail2.ru'
        )
        answer = Answer.objects.create(
            question=self.question,
            text='123',
            author=user
        )
        url = reverse("answer", kwargs={"pk": answer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
