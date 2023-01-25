import io
import datetime
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from src.profiles.models import FatUser, Social, Account, FatUserSocial, Social, Invitation,  Language
from src.questionnaire.models import Questionnaire
from src.team.models import Team, TeamMember
from src.repository.models import Category, Toolkit, Project, ProjectMember


def temporary_image_profiles():
    bts = io.BytesIO()
    img = Image.new("RGB", (100, 100))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())


def temporary_image_profiles2():
    bts = io.BytesIO()
    img = Image.new("RGB", (200, 200))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test2.jpg", bts.getvalue())


def temporary_image_profiles3():
    bts = io.BytesIO()
    img = Image.new("RGB", (100, 100))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test3.jpg", bts.getvalue())


def temporary_image():
    bts = io.BytesIO()
    img = Image.new("RGB", (250, 250))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())


def temporary_image_2():
    bts = io.BytesIO()
    img = Image.new("RGB", (500, 500))
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
            'birthday': datetime.date(1999, 12, 14),
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
            'birthday': datetime.date(1999, 12, 14),
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

    def test_questionnaire_create_invalid_birthday(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'description': 'test1',
            'country': 'test1',
            'town': 'test1',
            'phone': '+7999888',
            'birthday': datetime.date.today(),
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
            'birthday': datetime.date(1999, 12, 14),
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

    def test_questionnaire_invalid_team(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'description': 'test1',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998885544',
            'birthday': datetime.date(1999, 12, 14),
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
            'birthday': datetime.date(1999, 12, 14),
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
            'birthday': datetime.date(1999, 12, 14),
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
            'birthday': datetime.date(1999, 12, 14),
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
            'birthday': datetime.date(1999, 12, 14),
            'user': self.profile2.id,
            'languages': [self.language.id],
            'teams': [self.team2.id],
            'socials': [self.social2.id],
        }
        response = self.client.put(reverse('questionnaire_detail',
                                           kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='multipart'
                                   )
        self.assertEqual(len(response.data), 8)
        self.assertEqual(response.status_code, 200)

    def test_questionnaire_update_teams(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'user': self.profile2.id,
            'teams': [self.team2.id],
        }
        response = self.client.put(reverse('questionnaire_detail_teams',
                                           kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='multipart'
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_questionnaire_invalid_teams(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'user': self.profile2.id,
            'teams': [self.team3.id],
        }
        response = self.client.put(reverse('questionnaire_detail_teams',
                                   kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='json'
                                   )
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_update_projects(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'user': self.profile2.id,
            'projects': [self.project2.id],
        }
        response = self.client.put(reverse('questionnaire_detail_projects',
                                           kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='multipart'
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_questionnaire_invalid_projects(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'user': self.profile2.id,
            'projects': [self.project1.id],
        }
        response = self.client.put(reverse('questionnaire_detail_projects',
                                   kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='json'
                                   )
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_update_accounts(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'user': self.profile2.id,
            'accounts': [self.account2.id],
        }
        response = self.client.put(reverse('questionnaire_detail_accounts',
                                           kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='multipart'
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_questionnaire_update_invalid_birthday(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'description': 'test11',
            'country': 'test1',
            'town': 'test1',
            'phone': '+79998883333',
            'birthday': datetime.date.today(),
            'user': self.profile2.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'socials': [self.social2.id],
        }
        response = self.client.put(reverse('questionnaire_detail',
                                   kwargs={'pk': self.questionnaire2.id}),
                                   data=data,
                                   format='json'
                                   )
        self.assertEqual(response.status_code, 400)

    def test_questionnaire_update_invalid_phone(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'description': 'test11',
            'country': 'test1',
            'town': 'test1',
            'phone': '+7999888',
            'birthday': datetime.date(1999, 12, 14),
            'user': self.profile2.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'socials': [self.social2.id],
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
            'birthday': datetime.date(1999, 12, 14),
            'user': self.profile2.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'socials': [self.social1.id],
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
            'birthday': datetime.date(1999, 12, 14),
            'user': self.profile2.id,
            'toolkits': [self.toolkit1.id],
            'languages': [self.language.id],
            'socials': [self.social2.id],
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

    def test_avatar_update(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'user': self.profile2.id,
            'avatar': temporary_image_profiles3()
        }
        response = self.client.put(reverse('questionnaire_avatar',
                                            kwargs={'pk': self.questionnaire2.id}), data=data, format='multipart')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_avatar_update_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'user': self.profile1.id,
            'avatar': temporary_image_profiles3()
        }
        response = self.client.put(reverse('questionnaire_avatar',
                                            kwargs={'pk': self.questionnaire2.id}), data=data, format='multipart')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_avatar_update_invalid_format(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'user': self.profile2.id,
            'avatar': temporary_image_2()
        }
        response = self.client.put(reverse('questionnaire_avatar',
                                            kwargs={'pk': self.questionnaire2.id}), data=data, format='multipart')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 400)





