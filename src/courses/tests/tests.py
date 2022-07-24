from rest_framework import status
from rest_framework.test import APITestCase
from src.courses.models import Lesson, Course, Category, Quiz
from src.profiles.models import FatUser
from rest_framework.authtoken.models import Token


def create_user(name):
    user = FatUser.objects.create_user(
        username=name,
        password='password',
        email='email@mail.ru'
    )
    return user


def create_course():
    category = Category.objects.create(name='category1')
    course = Course.objects.create(
        name='first_course',
        description='description',
        slug='slug',
        author=create_user('user1'),
        mentor=create_user('user2'),
        category=category
    )
    return course


def create_lesson():
    lesson = Lesson.objects.create(
        name='first_lesson',
        course=create_course(),
        lesson_type='quiz',
    )
    return lesson


class AuthUserTestCase(APITestCase):

    def setUp(self):
        self.user = create_user('user3')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def test_help_mentor(self):
        lesson = create_lesson()
        data = {'lesson': f'{lesson.id}'}
        response = self.client.post('/courses/help_mentor/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_course(self):
        create_lesson()
        response = self.client.get('/courses/lesson/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_work_quiz(self):
        lesson = create_lesson()
        quiz = Quiz.objects.create(
            lesson=lesson,
            text='text',
            hint='hint',
        )
        data = {
            "lesson": f'{lesson.id}',
            'quiz_answer': f'{quiz.id}'
        }
        response = self.client.post('/courses/check_work/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')


class NotAuthUserTestCase(APITestCase):

    def test_student_work(self):
        lesson = create_lesson()
        quiz = Quiz.objects.create(
            lesson=lesson,
            text='text',
            hint='hint',
        )
        data = {
            "lesson": f'{lesson.id}',
            'quiz_answer': f'{quiz.id}'
        }
        response = self.client.post('/courses/check_work/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_course(self):
        create_lesson()
        response = self.client.get('/courses/lesson/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_lesson(self):
        create_lesson()
        response = self.client.get('/courses/lesson/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_help_mentor(self):
        lesson = create_lesson()
        data = {'lesson': f'{lesson.id}'}
        response = self.client.post('/courses/help_mentor/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_courses(self):
        create_course()
        response = self.client.get('/courses/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
