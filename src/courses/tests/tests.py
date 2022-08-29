from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from src.courses.models import Lesson, Course, Category
from src.profiles.models import FatUser


class TestCourses(APITestCase):

    def setUp(self):
        user_test1 = FatUser.objects.create_user(
            username='alexey',
            password='pwpk3oJ*T7',
            email='alexey@mail.ru'
        )
        user_test1.save()

        self.user_test1_token = Token.objects.create(user=user_test1)

        self.category = Category.objects.create(name='category1')
        self.course = Course.objects.create(
            id=1,
            name='Django blog',
            description='description',
            slug='slug',
            author=user_test1,
            category=self.category,

        )
        self.lesson = Lesson.objects.create(
            id=1,
            lesson_type="python",
            name='django',
            published='2022-08-29',
            slug='billie-jean',
            description='Lorem ipsum dolor sit amet.',
            course=self.course,
        )

    def test_get_courses_list(self):
        url = reverse("course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        url = reverse("course-detail", kwargs={"id": self.course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("name"), "Django blog")

    def test_get_course_detail_not_auth(self):
        url = reverse("course-detail", kwargs={"id": self.course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_course_detail_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        url = reverse("course-detail", kwargs={"id": 25})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_lesson_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        url = reverse("lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lesson_list_not_auth(self):
        url = reverse("lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_lesson_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        url = reverse("lesson-detail", kwargs={"id": self.lesson.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("lesson_type"), "python")
