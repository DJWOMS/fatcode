from django.urls import reverse
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
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_cat_list(self):
        response = self.client.get(reverse('cat_list'))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_cat_detail(self):
        response = self.client.get(reverse('cat_detail', kwargs={"pk": 1}))
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_cat_user_get(self):
        response = self.client.get(reverse('user_cat'))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    # TODO разобраться как получиь объект кота, сейчас в ответе возвращается 404 статус запроса
    # def test_cat_user_update(self):
    #     data = {
    #         "name": "барсик"
    #     }
    #     response = self.client.patch(reverse('cat_update', kwargs={'pk': 1}), data=data, format='json')
    #     self.assertEqual(response.status_code, 200)
