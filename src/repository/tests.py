import io
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


from src.profiles.models import FatUser, Account
from src.repository import models
from src.team.models import Team, TeamMember


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


class ProjectTest(APITestCase):
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

        self.profile3 = FatUser.objects.create(
            username='username3',
            email='test3@mail.ru',
            password='test3'
        )
        self.profile3.save()
        self.profile3_token = Token.objects.create(user=self.profile3)

        self.account = Account.objects.create(
            user=self.profile1,
            provider='github',
            account_id='93525670',
            account_url='https://github.com/veraandrianova',
            account_name='veraandrianova'
        )
        self.account.save()

        self.team1 = Team.objects.create(
            name='team1',
            user=self.profile1
        )
        self.team1.save()

        self.team2 = Team.objects.create(
            name='team2',
            user=self.profile1
        )

        self.team3 = Team.objects.create(
            name='team3',
            user=self.profile2
        )

        self.team4 = Team.objects.create(
            name='team4',
            user=self.profile1
        )

        self.team5 = Team.objects.create(
            name='team5',
            user=self.profile1
        )

        self.team_member1 = TeamMember.objects.create(
            team=self.team1,
            user=self.profile2
        )

        self.team_member2 = TeamMember.objects.create(
            team=self.team4,
            user=self.profile2
        )

        self.category = models.Category.objects.create(
            name='category1'
        )
        self.category.save()

        self.toolkit1 = models.Toolkit.objects.create(
            name='toolkit1'
        )
        self.toolkit1.save()

        self.toolkit2 = models.Toolkit.objects.create(
            name='toolkit2'
        )

        self.project1 = models.Project.objects.create(
            name='project1',
            description='test1',
            avatar=temporary_image(),
            user=self.profile1,
            category=self.category,
            repository='https://github.com/veraandrianova/oop_1'
        )
        self.project1.teams.add(self.team4)
        self.project1.toolkit.add(self.toolkit1)
        self.project1.save()

        self.project2 = models.Project.objects.create(
            name='project2',
            description='test2',
            user=self.profile1,
            category=self.category,
            repository='https://github.com/veraandrianova/flask'
        )
        self.project1.teams.add(self.team5)
        self.project1.toolkit.add(self.toolkit1)
        self.project1.save()

    def test_category_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('category'))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_toolkit_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('toolkit'))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_my_projects_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('my_projects'))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_my_projects_no_authorization(self):
        response = self.client.delete(reverse('my_projects'))
        self.assertEqual(response.status_code, 405)

    def test_projects_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('project'))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_projects_list_no_authorization(self):
        response = self.client.delete(reverse('project'))
        self.assertEqual(response.status_code, 405)

    def test_project_create(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'project',
            'description': 'test1',
            'toolkit': [self.toolkit1.id],
            'category': self.category.id,
            'teams': [self.team1.id],
            'repository': 'https://github.com/veraandrianova/drf_git'
        }
        response = self.client.post(reverse('project'), data=data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), 7)

    def test_project_create_invalid_repo(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'project',
            'description': 'test1',
            'toolkit': [self.toolkit1.id],
            'category': self.category.id,
            'teams': [self.team2.id],
            'repository': 'https://github.com/veraandrianova/oop_1'
        }
        response = self.client.post(reverse('project'), data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_project_create_invalid_team(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'project',
            'description': 'test1',
            'toolkit': [self.toolkit1.id],
            'category': self.category.id,
            'teams': [self.team4.id],
            'repository': 'https://github.com/veraandrianova/rest_toy_shop'
        }
        response = self.client.post(reverse('project'), data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_project_create_invalid_repo_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'project',
            'description': 'test1',
            'toolkit': [self.toolkit1.id],
            'category': self.category.id,
            'teams': [self.team1.id],
            'repository': 'https://github.com/veraandrianova/rest'
        }
        response = self.client.post(reverse('project'), data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_project_create_invalid_team_not_author(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'project',
            'description': 'test1',
            'toolkit': [self.toolkit1.id],
            'category': self.category.id,
            'teams': [self.team3.id],
            'repository': 'https://github.com/veraandrianova/drf_git'
        }
        response = self.client.post(reverse('project'), data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_project_create_no_authorization(self):
        data = {
            'name': 'project',
            'description': 'test1',
            'toolkit': [self.toolkit1.id],
            'category': self.category.id,
            'teams': [self.team1.id],
            'repository': 'https://github.com/veraandrianova/rest'
        }
        response = self.client.post(reverse('project'), data=data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_project_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('project_detail', kwargs={'pk': self.project1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Project.objects.count(), 2)

    def test_project_detail_no_author(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.get(reverse('project_detail', kwargs={'pk': self.project1.id}))
        self.assertEqual(response.status_code, 200)

    def test_project_detail_no_authorization(self):
        response = self.client.get(reverse('project_detail', kwargs={'pk': self.project1.id}))
        self.assertEqual(response.status_code, 401)

    def test_project_update(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'test',
            'description': 'test1',
            'toolkit': [self.toolkit1.id],
            'category': self.category.id,
            'teams': [self.team1.id],
            'repository': 'https://github.com/veraandrianova/drf_git'
        }
        response = self.client.put(reverse('project_detail',
                                           kwargs={'pk': self.project1.id}),
                                   data=data,
                                   format='multipart'
                                   )
        self.assertEqual(len(response.data), 7)
        self.assertEqual(response.status_code, 200)

    def test_project_update_invalid_repo_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'test',
            'description': 'test1',
            'toolkit': [self.toolkit1.id],
            'category': self.category.id,
            'teams': [self.team1.id],
            'repository': 'https://github.com/veraandrianova/123'
        }
        response = self.client.put(reverse('project_detail',
                                           kwargs={'pk': self.project1.id}),
                                   data=data,
                                   format='json'
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 400)

    def test_project_update_invalid_repo(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'test',
            'description': 'test1',
            'toolkit': [self.toolkit1.id],
            'category': self.category.id,
            'teams': [self.team1.id],
            'repository': 'https://github.com/veraandrianova/flask'
        }
        response = self.client.put(reverse('project_detail',
                                           kwargs={'pk': self.project1.id}),
                                   data=data,
                                   format='json'
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 400)

    def test_project_update_invalid_team(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'test',
            'description': 'test1',
            'toolkit': [self.toolkit1.id],
            'category': self.category.id,
            'teams': [self.team4.id],
            'repository': 'https://github.com/veraandrianova/123'
        }
        response = self.client.put(reverse('project_detail',
                                           kwargs={'pk': self.project1.id}),
                                   data=data,
                                   format='json'
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 400)

    def test_project_update_invalid_team_no_author(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'test',
            'description': 'test1',
            'toolkit': [self.toolkit1.id],
            'category': self.category.id,
            'teams': [self.team3.id],
            'repository': 'https://github.com/veraandrianova/123'
        }
        response = self.client.put(reverse('project_detail',
                                           kwargs={'pk': self.project1.id}),
                                   data=data,
                                   format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 400)

    def test_project_update_no_authorization(self):
        data = {
            'name': 'test',
            'description': 'test1',
            'toolkit': [self.toolkit1.id],
            'category': self.category.id,
            'teams': [self.team3.id],
            'repository': 'https://github.com/veraandrianova/123'
        }
        response = self.client.put(reverse('project_detail',
                                           kwargs={'pk': self.project1.id}),
                                   data=data,
                                   format='json')
        self.assertEqual(response.status_code, 401)

    def test_project_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.delete(reverse('project_detail', kwargs={'pk': self.project1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Project.objects.filter(id=self.project1.id).exists(), False)

    def test_project_delete_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.delete(reverse('project_detail', kwargs={'pk': self.project1.id}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(models.Project.objects.filter(id=self.project1.id).exists(), True)

    def test_project_teams_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('project_teams', kwargs={'pk': self.project1.id}))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_project_teams_member(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.get(reverse('project_teams', kwargs={'pk': self.project1.id}))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_project_teams_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.get(reverse('project_teams', kwargs={'pk': self.project1.id}))
        self.assertEqual(response.status_code, 403)

    def test_project_board_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('project_board', kwargs={'pk': self.project1.id}))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_project_board_member(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.get(reverse('project_board', kwargs={'pk': self.project1.id}))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_project_board_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.get(reverse('project_board', kwargs={'pk': self.project1.id}))
        self.assertEqual(response.status_code, 403)

    def test_avatar_update(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'user': self.profile1.id,
            'avatar': temporary_image_3()
        }
        response = self.client.put(reverse('project_avatar',
                                            kwargs={'pk': self.project1.id}), data=data, format='multipart')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_avatar_update_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'user': self.profile2.id,
            'avatar': temporary_image_3()
        }
        response = self.client.put(reverse('project_avatar',
                                            kwargs={'pk': self.project1.id}), data=data, format='multipart')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_avatar_update_invalid_format(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'user': self.profile1.id,
            'avatar': temporary_image_2()
        }
        response = self.client.put(reverse('project_avatar',
                                            kwargs={'pk': self.project1.id}), data=data, format='multipart')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 400)
