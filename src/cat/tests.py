from rest_framework.test import APITestCase
from src.profiles.models import FatUser
from rest_framework.authtoken.models import Token


def create_user(email, name):
    user = FatUser.objects.create_user(
        username=name,
        password='password',
        email=email
    )
    return user


class CatTestCase(APITestCase):

    def setUp(self):
        self.user = create_user('zxczxczxczxxx', 'oaidoasdioasdois@mail.ru')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

#
#     def test_detail_course(self):
#         create_lesson()
#         response = self.client.get('/courses/lesson/1/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
