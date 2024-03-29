from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from src.courses.models import Lesson, Course, Category, Tag
from src.profiles.models import FatUser
from src.courses import serializers


# TODO Добавить тесты
class TestCoursesAPI(APITestCase):

    def setUp(self):
        user_test1 = FatUser.objects.create_user(
            username='alexey',
            password='pwpk3oJ*T7',
            email='alexey@mail.ru'
        )
        user_test1.save()

        self.user_test1_token = Token.objects.create(user=user_test1)

        self.category = Category.objects.create(name='category1')
        self.category_child = Category.objects.create(name='category2', parent=self.category)
        self.course = Course.objects.create(
            name='Django blog',
            description='description',
            slug='slug',
            author=user_test1,
            category=self.category
        )
        self.lesson = Lesson.objects.create(
            lesson_type="python",
            name='django',
            published='2022-08-29',
            slug='billie-jean',
            description='Lorem ipsum dolor sit amet.',
            course=self.course
        )

        self.tag = Tag.objects.create(name='Django')

    def test_get_courses_list(self):
        response = self.client.get(reverse("courses"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_course_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(reverse("course", kwargs={"pk": self.course.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("name"), "Django blog")

    def test_get_course_detail_not_auth(self):
        response = self.client.get(reverse("course", kwargs={"pk": self.course.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_course_detail_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(reverse("course", kwargs={"pk": 25}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_lesson_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(reverse("lesson", kwargs={"pk": self.lesson.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("lesson_type"), "python")

    def test_get_lesson_not_auth(self):
        response = self.client.get(reverse("lesson", kwargs={"pk": self.lesson.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_categories(self):
        response = self.client.get(reverse("get-categories"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["name"], "category1")

    def test_get_categories_children(self):
        response = self.client.get(reverse("get-categories"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.json().get("results")[0]['children'][0]["name"], "category2")

    def test_get_tags(self):
        response = self.client.get(reverse("get-tags"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["name"], "Django")
