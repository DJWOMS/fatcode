from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from src.profiles.models import FatUser, Social


class ProfileTests(APITestCase):
    user_create_data = {
        'username': 'anton',
        'password': 'V97tn7M4rU',
        're_password': 'V97tn7M4rU',
        'email': 'anton@example.com'
    }

    def test_create_user(self):
        request = self.client.post(
                '/auth/users/',
                self.user_create_data,
                format='json'
        )

        user = FatUser.objects.get(username='anton')

        self.assertEqual(user.username, 'anton')
        self.assertEqual(user.email, 'anton@example.com')

    def test_create_user_error(self):
        request = self.client.post('/auth/users/', {}, format='json')
        self.assertEqual(request.status_code, 400)
        self.assertEqual(request.data[
            'non_field_errors'][0].title(),
            'Два Пароля Не Совпадают.')


