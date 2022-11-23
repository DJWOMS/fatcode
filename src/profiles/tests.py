import io
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from src.profiles.models import FatUser, Social

user_create_data = {
    'username': 'anton',
    'password': 'V97tn7M4rU',
    're_password': 'V97tn7M4rU',
    'email': 'antonenique@example.com'
}

image = io.BytesIO()
Image.new("RGB", (100, 100)).save(image, "JPEG")

avatar_file = SimpleUploadedFile("avatar.jpg", image.getvalue())


class ProfileRegTests(APITestCase):
    def test_create_user(self):
        self.client.post('/api/v1/auth/users/', user_create_data, format='json')
        user = FatUser.objects.get(email='antonenique@example.com')
        self.assertEqual(user.username, 'anton')
        self.assertEqual(user.email, 'antonenique@example.com')

    def test_create_user_error_pass(self):
        data = user_create_data.copy()
        data['re_password'] = 'V97tn7M4ru'
        request = self.client.post('/api/v1/auth/users/', data, format='json')
        self.assertEqual(request.status_code, 400)
        self.assertEqual(request.data['non_field_errors'][0].title(), 'Два Пароля Не Совпадают.')

    def test_create_user_required(self):
        error_msg = 'Обязательное Поле.'
        response = self.client.post('/api/v1/auth/users/', {}, format='json')
        self.assertEqual(response.data['email'][0].title(), error_msg)
        self.assertEqual(response.data['username'][0].title(), error_msg)
        self.assertEqual(response.data['password'][0].title(), error_msg)
        self.assertEqual(response.data['re_password'][0].title(), error_msg)

    def test_create_user_unique_name(self):
        self.client.post('/api/v1/auth/users/', user_create_data, format='json')
        response = self.client.post('/api/v1/auth/users/', user_create_data, format='json')
        self.assertEqual(
            response.data['username'][0].title(),
            'Пользователь С Таким Именем Уже Существует.'
        )

    # TODO написать тест для проверки почты, почта уже существует
    def test_create_user_unique_email(self):
        pass


class ProfileAuthTests(APITestCase):
    def setUp(self):
        self.client.post('/api/v1/auth/users/', user_create_data, format='json')
        url = "/api/v1/auth/token/login/"
        user = {
            'username': user_create_data['username'],
            'password': user_create_data['password']
        }
        response = self.client.post(url, user, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('auth_token' in response.data)

    def test_user_pub_profile(self):
        user = FatUser.objects.get(username='anton')
        url = reverse("user-pub", kwargs={"pk": user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('email' in response.data)

    def test_user_profile(self):
        user = FatUser.objects.get(username='anton')
        url = reverse("user")
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('email' in response.data)


class TestSocial(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        Social.objects.create(title='Social 1')
        Social.objects.create(title='Social 2')

    def test_social_list(self):
        url = reverse("social-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 2)

    def test_social_detail(self):
        social = Social.objects.get(title='Social 1')
        url = reverse("social-detail", kwargs={"pk": social.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("title"), 'Social 1')


class FatUserProfileTest(APITestCase):

    def setUp(self):
        self.user_test1 = FatUser.objects.create_user(
            username='alexey',
            password='pwpk3oJ*T7',
            email='alexey@mail.ru'
        )
        self.user_test1.save()

        self.user_test1_token = Token.objects.create(user=self.user_test1)

        avatar = io.BytesIO()
        Image.new("RGB", (100, 100)).save(avatar, "JPEG")
        self.avatar_file = SimpleUploadedFile("avatar.jpg", image.getvalue())

    def test_user_avatar_post(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        url = reverse("user-avatar")
        data = {
            "id": self.user_test1.id,
            "avatar": self.avatar_file,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_avatar_post_not_auth(self):
        url = reverse("user-avatar")
        data = {
            "id": self.user_test1.id,
            "avatar": self.avatar_file,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_avatar_put(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        url = reverse("user-avatar")
        data = {
            "id": self.user_test1.id,
            "avatar": self.avatar_file,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_avatar_put_not_auth(self):
        url = reverse("user-avatar")
        data = {
            "id": self.user_test1.id,
            "avatar": self.avatar_file,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
