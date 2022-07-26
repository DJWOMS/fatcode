from rest_framework import status
from rest_framework.test import APITestCase
from .models import Question, QuestionReview, AnswerReview, Answer, Tags
from src.profiles.models import FatUser
from rest_framework.authtoken.models import Token
from . import serializers


class QuestionApiViewTestCase(APITestCase):
    def setUp(self):
        self.user = FatUser.objects.create_user(
            username='user',
            password='password',
            email='email@mail.ru'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.question = Question.objects.create(
            title='title1',
            author=self.user,
            text='text',
        )

    def test_get_question_list(self):
        response = self.client.get('/questions/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_answer(self):
        data = {
            'question': self.question.id,
            'text': 'text_for_answer'
        }
        response = self.client.post('/questions/create_answer/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_detail_question(self):
        response = self.client.get(f'/questions/detail/{self.question.id}/')
        serialize = serializers.RetrieveQuestionSerializer(self.question)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialize.data)

    def create_objectAnswer(self):
        answer = Answer.objects.create(
            question=self.question,
            text='123',
            author=self.user
        )
        return answer

    def test_update_question(self):
        data = {
            'text': 'title2',
        }
        response = self.client.patch(f'/questions/update_question/{self.question.id}/', data)
        self.question = Question.objects.get(id=self.question.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.question.text, data['text'])

    def test_update_answer(self):
        data = {
            'text': 'updated_text'
        }
        answer = Answer.objects.create(
            author=self.question.author,
            text='created_text',
            question=self.question
        )
        response = self.client.patch(f'/questions/update_answer/{answer.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

