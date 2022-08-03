from rest_framework import status
from rest_framework.test import APITestCase
from .models import Question, QuestionReview, AnswerReview, Answer
from src.profiles.models import FatUser
from rest_framework.authtoken.models import Token
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
        self.question = Question.objects.create(
            title='title1',
            author=self.user,
            text='text',
        )

    def test_get_question_list(self):
        response = self.client.get('/api/v1/questions/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_answer(self):
        data = {
            'question': self.question.id,
            'text': 'text_for_answer'
        }
        response = self.client.post('/api/v1/questions/create_answer/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_detail_question(self):
        response = self.client.get(f'/api/v1/questions/detail/{self.question.id}/')
        serialize = serializers.RetrieveQuestionSerializer(self.question)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialize.data)

    def test_update_question(self):
        data = {
            'text': 'text2'
        }
        response = self.client.patch(f'/api/v1/questions/update_question/{self.question.id}/', data)
        self.question = Question.objects.get(id=self.question.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.question.text, data['text'])

    def test_update_answer(self):
        data = {
            'text': 'updated_text'
        }
        answer = self.create_answerObject()
        response = self.client.patch(f'/api/v1/questions/update_answer/{answer.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_answer(self):
        answer = self.create_answerObject()
        response = self.client.delete(f'/api/v1/questions/delete_answer/{answer.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Answer.objects.exists(), False)

    def test_delete_question(self):
        response = self.client.delete(f'/api/v1/questions/delete_question/{self.question.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.exists(), False)

    def test_question_review(self):
        data = {
            'grade': 'false',
            'question': self.question.id,
        }
        response = self.client.post('/api/v1/questions/question_review/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_repeat_question_review(self):
        review = QuestionReview.objects.create(
            question=self.question,
            user=self.user,
            grade=False
        )
        data = {
            'grade': False,
            'question': self.question.id,
        }
        response = self.client.post('/api/v1/questions/question_review/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_review(self):
        answer = self.create_answerObject()
        data = {
            'grade': False,
            'answer': f'{answer.id}',
        }
        response = self.client.post('/api/v1/questions/answer_review/', data)
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

        response = self.client.delete(f'/api/v1/questions/delete_answer/{answer.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

