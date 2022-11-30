import io
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from src.profiles.models import FatUser, Social, Questionnaire, Language, Account, FatUserSocial, Social
from src.team.models import Team, TeamMember
from src.repository.models import Category, Toolkit, Project, ProjectMember

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
        self.client.post('/api/v1/auth/users/', user_create_data, format='json')
        response = self.client.post('/api/v1/auth/users/', user_create_data, format='json')
        self.assertEqual(
            response.data['email'][0].title(),
            'Пользователь С Таким Email Уже Существует.')


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


class ProfileAuthTests(APITestCase):
    def setUp(self):
        self.client.post('/api/v1/auth/users/', user_create_data, format='json')
        url = "/api/v1/auth/token/login/"
        user = {
            'email': user_create_data['email'],
            'password': user_create_data['password']
        }
        request = self.client.post(url, user, format='json')
        self.assertEqual(request.status_code, 200)
        self.assertTrue('auth_token' in request.data)

    def test_user_pub_profile(self):
        user = FatUser.objects.get(username='anton')
        url = reverse("user-pub", kwargs={"pk": user.pk})
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertFalse('email' in request.data)

    def test_user_profile(self):
        user = FatUser.objects.get(username='anton')
        url = reverse("user")
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertTrue('email' in request.data)


class TestSocial(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        Social.objects.create(title='Social 1')
        Social.objects.create(title='Social 2')

    def test_social_list(self):
        url = reverse("social-list")
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 2)

    def test_social_detail(self):
        social = Social.objects.get(title='Social 1')
        url = reverse("social-detail", kwargs={"pk": social.pk})
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['title'], 'Social 1')


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


def temporary_image():
    bts = io.BytesIO()
    img = Image.new("RGB", (250, 250))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())

def temporary_image_2():
    bts = io.BytesIO()
    img = Image.new("RGB", (300, 300))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test2.jpg", bts.getvalue())

def temporary_image_3():
    bts = io.BytesIO()
    img = Image.new("RGB", (250, 250))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test3.jpg", bts.getvalue())


class QuestionnaireTest(APITestCase):
    def setUp(self):
        self.profile1 = FatUser.objects.create(
            username='username1',
            email='test1@mail.ru',
            password='test1'
        )
        self.profile1.save()
        self.profile1_token = Token.objects.create(user=self.profile1)

        self.profile2 = FatUser.objects.create(
            username='username2',
            email='test2@mail.ru',
            password='test2'
        )
        self.profile2.save()
        self.profile2_token = Token.objects.create(user=self.profile2)

        self.account1 = Account.objects.create(
            user=self.profile1,
            provider='github',
            account_id='93525670',
            account_url='https://github.com/veraandrianova',
            account_name='veraandrianova'
        )
        self.account1.save()

        self.account2 = Account.objects.create(
            user=self.profile2,
            provider='github',
            account_id='22085473',
            account_url='https://github.com/DJWOMS',
            account_name='DJWOMS'
        )
        self.account2.save()

        self.team1 = Team.objects.create(
            name='team1',
            user=self.profile1
        )
        self.team1.save()

        self.team2 = Team.objects.create(
            name='team2',
            user=self.profile2
        )

        self.team3 = Team.objects.create(
            name='team3',
            user=self.profile1
        )

        self.team_member1 = TeamMember.objects.create(
            team=self.team1,
            user=self.profile2
        )

        self.category = Category.objects.create(
            name='category1'
        )
        self.category.save()

        self.toolkit1 = Toolkit.objects.create(
            name='toolkit1'
        )
        self.toolkit1.save()

        self.project1 = Project.objects.create(
            name='project1',
            description='test1',
            user=self.profile1,
            category=self.category,
            repository='https://github.com/veraandrianova/oop_1'
        )
        self.project1.teams.add(self.team1)
        self.project1.toolkit.add(self.toolkit1)
        self.project1.save()

        self.project2 = Project.objects.create(
            name='project2',
            description='test2',
            user=self.profile2,
            category=self.category,
            repository='https://github.com/veraandrianova/flask'
        )
        self.project2.teams.add(self.team2)
        self.project2.toolkit.add(self.toolkit1)
        self.project2.save()

        self.social_all = Social.objects.create(
            title='test',
            url='https://vk.com/'
        )

        self.social1 = FatUserSocial.objects.create(
            social=self.social_all,
            user=self.profile1,
            user_url='https://vk1.com/'
        )

        self.social2 = FatUserSocial.objects.create(
            social=self.social_all,
            user=self.profile2,
            user_url='https://vk2.com/'
        )

        self.language = Language.objects.create(
            name='test',
        )

        self.questionnaire2 = Questionnaire.objects.create(
            description='description2',
            country='test',
            town='test',
            phone='+79998887766',
            avatar=temporary_image(),
            user=self.profile2
        )
        self.questionnaire2.teams.add(self.team2)
        self.questionnaire2.toolkits.add(self.toolkit1)
        self.questionnaire2.projects.add(self.project2)
        self.questionnaire2.accounts.add(self.account2)
        self.questionnaire2.languages.add(self.language)
        self.questionnaire2.socials.add(self.social2)
        self.project1.save()


    def test_questionnaire_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('questionnaire'))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_questionnaire_list__no_authorization(self):
        response = self.client.delete(reverse('questionnaire'))
        self.assertEqual(response.status_code, 405)

    def test_questionnaire_create(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'description': 'test1',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'avatar': temporary_image(),
            'user': self.profile1.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project1.id],
            'teams': [self.team1.id],
            'socials': [self.social1.id],
            'accounts': [self.account1.id]
        }
        response = self.client.post(reverse('questionnaire'), data=data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), 11)

    def test_questionnaire_create_invalid_phone(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'description': 'test1',
            'country': 'test1',
            'town': 'test1',
            'phone': '+7999888',
            'user': self.profile1.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project1.id],
            'teams': [self.team1.id],
            'socials': [self.social1.id],
            'accounts': [self.account1.id]
        }
        response = self.client.post(reverse('questionnaire'), data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_create_invalid_project(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'description': 'test1',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'user': self.profile1.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project2.id],
            'teams': [self.team1.id],
            'socials': [self.social1.id],
            'accounts': [self.account1.id]
        }
        response = self.client.post(reverse('questionnaire'), data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_invalide_team(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'description': 'test1',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'user': self.profile1.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project1.id],
            'teams': [self.team2.id],
            'socials': [self.social1.id],
            'accounts': [self.account1.id]
        }
        response = self.client.post(reverse('questionnaire'), data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_invalid_social(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'description': 'test1',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'user': self.profile1.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project1.id],
            'teams': [self.team1.id],
            'socials': [self.social2.id],
            'accounts': [self.account1.id]
        }
        response = self.client.post(reverse('questionnaire'), data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_invalid_account(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'description': 'test1',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'user': self.profile1.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project1.id],
            'teams': [self.team1.id],
            'socials': [self.social1.id],
            'accounts': [self.account2.id]
        }
        response = self.client.post(reverse('questionnaire'), data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_invalid_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'description': 'test1',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'user': self.profile2.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project2.id],
            'teams': [self.team2.id],
            'socials': [self.social2.id],
            'accounts': [self.account2.id]
        }
        response = self.client.post(reverse('questionnaire'), data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_update(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'description': 'test11',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'avatar': temporary_image_3(),
            'user': self.profile2.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project2.id],
            'teams': [self.team2.id],
            'socials': [self.social2.id],
            'accounts': [self.account2.id]
        }
        response = self.client.put(reverse('questionnaire_detail',
                                   kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='multipart'
                                   )
        self.assertEqual(len(response.data), 11)
        self.assertEqual(response.status_code, 200)

    def test_questionnaire_update_invalid_avatar(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'description': 'test11',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'avatar': temporary_image_2(),
            'user': self.profile2.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project2.id],
            'teams': [self.team2.id],
            'socials': [self.social2.id],
            'accounts': [self.account2.id]
        }
        response = self.client.put(reverse('questionnaire_detail',
                                   kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='multipart'
                                   )
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_update_invalid_phone(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'description': 'test11',
            'country': 'test1',
            'town': 'test1',
            'phone': '+7999888',
            'user': self.profile2.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project2.id],
            'teams': [self.team2.id],
            'socials': [self.social2.id],
            'accounts': [self.account2.id]
        }
        response = self.client.put(reverse('questionnaire_detail',
                                   kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='json'
                                   )
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_invalid_project(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'description': 'test11',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'user': self.profile2.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project1.id],
            'teams': [self.team2.id],
            'socials': [self.social2.id],
            'accounts': [self.account2.id]
        }
        response = self.client.put(reverse('questionnaire_detail',
                                   kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='json'
                                   )
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_invalid_team(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'description': 'test11',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'user': self.profile2.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project2.id],
            'teams': [self.team3.id],
            'socials': [self.social2.id],
            'accounts': [self.account2.id]
        }
        response = self.client.put(reverse('questionnaire_detail',
                                   kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='json'
                                   )
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_update_invalid_social(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'description': 'test11',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'user': self.profile2.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project2.id],
            'teams': [self.team2.id],
            'socials': [self.social1.id],
            'accounts': [self.account2.id]
        }
        response = self.client.put(reverse('questionnaire_detail',
                                   kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='json'
                                   )
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_account(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'description': 'test11',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'user': self.profile2.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project2.id],
            'teams': [self.team2.id],
            'socials': [self.social2.id],
            'accounts': [self.account1.id]
        }
        response = self.client.put(reverse('questionnaire_detail',
                                   kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='json'
                                   )
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_invalid_author(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'description': 'test11',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'user': self.profile2.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'projects': [self.project2.id],
            'teams': [self.team2.id],
            'socials': [self.social2.id],
            'accounts': [self.account2.id]
        }
        response = self.client.put(reverse('questionnaire_detail',
                                   kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='json'
                                   )
        self.assertEqual(response.status_code, 403)

    def test_questionnaire_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.delete(reverse('questionnaire_detail', kwargs={'pk': self.questionnaire2.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Questionnaire.objects.filter(id=self.project1.id).exists(), False)

    def test_questionnaire_delete_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.delete(reverse('questionnaire_detail', kwargs={'pk': self.questionnaire2.id}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Questionnaire.objects.filter(id=self.questionnaire2.id).exists(), True)




