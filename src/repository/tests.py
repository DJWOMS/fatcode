from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from src.profiles.models import FatUser, Account
from src.repository.models import Project, Toolkit, Category, ProjectMember
from src.team.models import Team, TeamMember

class TeamTest(APITestCase):
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

        self.team_member1 = TeamMember.objects.create(
            team=self.team1,
            user=self.profile2
        )

        self.team_member2 = TeamMember.objects.create(
            team=self.team4,
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

        self.toolkit2 = Toolkit.objects.create(
            name='toolkit2'
        )

        self.project1 = Project.objects.create(
            name='project1',
            description='test1',
            user=self.profile1,
            category=self.category,
            repository='https://github.com/veraandrianova/oop_1'
        )
        self.project1.teams.add(self.team4)
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

    ##TODO почему 400?
    def test_project_create(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'project',
            'description': 'test1',
            'toolkit': self.toolkit1,
            'category': self.category,
            'teams': self.team1.id,
            'repository': 'https://github.com/veraandrianova/drf_git'
        }
        response = self.client.post(reverse('project'), data=data, format='json')
        print(data)
        self.assertEqual(response.status_code, 201)
        print(response.text)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(Project.objects.count(), 4)

    def test_project_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('project_detail', kwargs={'pk': self.project1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 1)

    def test_project_detail_no_author(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.get(reverse('project_detail', kwargs={'pk': self.project1.id}))
        self.assertEqual(response.status_code, 200)

    def test_project_detail_no_authorization(self):
        response = self.client.get(reverse('project_detail', kwargs={'pk': self.project1.id}))
        self.assertEqual(response.status_code, 401)
##TODO почему 400?
    # def test_project_update(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
    #     data = {
    #         'name': 'test',
    #         'description': 'test1',
    #         'toolkit': self.toolkit1.id,
    #         'category': self.category.id,
    #         'teams': self.team1.id,
    #         'repository': 'https://github.com/veraandrianova/oop_1'
    #     }
    #     response = self.client.put(reverse('project_detail', kwargs={'pk': self.project1.id}), data=data, format='json')
    #     self.assertEqual(len(response.data), 2)
    #     self.assertEqual(response.status_code, 200)

    def test_project_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.delete(reverse('project_detail', kwargs={'pk': self.project1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.filter(id=self.project1.id).exists(), False)

    def test_project_delete_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.delete(reverse('project_detail', kwargs={'pk': self.project1.id}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Project.objects.filter(id=self.project1.id).exists(), True)

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