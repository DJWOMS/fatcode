from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from src.profiles.models import FatUser
from src.team.models import Post, Comment, Team, TeamMember, Invitation, SocialLink

from src.team import serializers


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

        self.profile4 = FatUser.objects.create(
            username='username4',
            email='test4@mail.ru',
            password='test4'
        )
        self.profile4.save()

        self.team1 = Team.objects.create(
            name='team1',
            user=self.profile1
        )
        self.team_member1 = TeamMember.objects.create(
            team=self.team1,
            user=self.profile3
        )
        self.team2 = Team.objects.create(
            name='team2',
            user=self.profile2
        )
        self.team3 = Team.objects.create(
            name='team3',
            user=self.profile1
        )
        self.invitation = Invitation.objects.create(
            user=self.profile2,
            team=self.team3
        )

        self.post1 = Post.objects.create(
            text='text1',
            user=self.profile1,
            team=self.team1
        )
        # self.post2 = Post.objects.create(
        #     text='text2',
        #     user=self.profile3,
        #     team=self.team1
        # )
        # self.comment1 = Comment.objects.create(
        #     user=self.profile1,
        #     post=self.post1,
        #     text='text1',
        # )
        # self.comment2 = Comment.objects.create(
        #     user=self.profile2,
        #     post=self.post1,
        #     text='text2',
        # )

    def test_team_create_invalid(self):
        data = {
            'name': 'test',
            'user': self.profile4.id
        }
        response = self.client.post(reverse('teams'), data=data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_team_create(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'name1',
            'user': self.profile1.id
        }
        response = self.client.post(reverse('teams'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(Team.objects.count(), 4)

    def test_team_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('teams'))
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, 200)

    def test_team_list_no_authorization(self):
        response = self.client.get(reverse('teams'))
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, 200)

    def test_team_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('detail_teams', kwargs={'pk': self.team1.id}))
        self.assertEqual(response.status_code, 200)

    def test_team_detail_no_authorization(self):
        response = self.client.get(reverse('detail_teams', kwargs={'pk': self.team1.id}))
        self.assertEqual(response.status_code, 200)

    def test_team_update(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'name_test',
            'user': self.profile1.id
        }
        response = self.client.put(reverse('detail_teams', kwargs={'pk': self.team1.id}), data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_team_update_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'name': 'test',
            'user': self.profile2.id
        }
        response = self.client.put(reverse('detail_teams', kwargs={'pk': self.team1.id}), data=data, format='json')
        team = Team.objects.get(id=self.team1.id)
        self.assertEqual(response.status_code, 403)
    ##TODO AssertionError: Expected a `Response`, `HttpResponse` or `HttpStreamingResponse` to be returned from the view, but received a `<class 'NoneType'>`

    # def test_team_delete(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
    #     response = self.client.delete(reverse('detail_teams', kwargs={'pk': self.team1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Team.objects.exists(), False)

    def test_team_delete_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.delete(reverse('detail_teams', kwargs={'pk': self.team1.id}))
        self.assertEqual(response.status_code, 403)

    def test_team_detail_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('detail_teams', kwargs={'pk': 50}))
        self.assertEqual(response.status_code, 404)

    def test_my_team(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('my_team'))
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_my_team_no_authorization(self):
        response = self.client.get(reverse('my_team'))
        self.assertEqual(response.status_code, 401)

    def test_member_team(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.get(reverse('team_member'))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_member_team_no_authorization(self):
        response = self.client.get(reverse('team_member'))
        self.assertEqual(response.status_code, 401)

    def test_invitation_invalid(self):
        data = {
            'team': self.team1.id,
            'user': self.profile4.id
        }
        response = self.client.post(reverse('invitation'), data=data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_invitation(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'team': self.team1.id,
            'user': self.profile2.id
        }
        response = self.client.post(reverse('invitation'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(Invitation.objects.count(), 2)

    ##TODO неправильно возращается статус невозможно доавиться к себе в команду
    # def test_invitation_forbidden(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
    #     data = {
    #         'team': self.team1.id,
    #         'user': self.profile1.id
    #     }
    #     response = self.client.post(reverse('invitation'), data=data, format='json')
    #     print(response)
    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(Invitation.objects.count(), 1)

    def test_invitation_no_authorization(self):
        response = self.client.get(reverse('invitation'))
        self.assertEqual(response.status_code, 401)
#     #TODO django.urls.exceptions.NoReverseMatch: Reverse for 'invitation_delete' with no arguments not found.
    # def test_my_invitation_detail(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
    #     invitation = Invitation.objects.create(
    #         team=self.team3,
    #         user=self.profile3,
    #     )
    #     print('invitation', invitation.id)
    #     response = self.client.get(reverse('invitation_delete'), kwargs={'pk': invitation.id})
    #     print(response.data)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.status_code, 200)
    #     #TODO django.urls.exceptions.NoReverseMatch: Reverse for 'invitation_delete' with no arguments not found.
    # def test_invitation_delete(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
    #     response = self.client.delete(reverse('invitation_delete'), kwargs={'pk': self.invitation.id})
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Invitation.objects.exists(), False)
    #     #TODO django.urls.exceptions.NoReverseMatch: Reverse for 'invitation_delete' with no arguments not found.
    # def test_invitation_delete_invalid(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
    #     response = self.client.delete(reverse('invitation_delete'), kwargs={'pk': self.invitation.id})
    #     self.assertEqual(response.status_code, 403)
    def test_invitation_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('invitation_list'))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_invitation_list_no_authorization(self):
        response = self.client.get(reverse('invitation_list'))
        self.assertEqual(response.status_code, 401)
    # ##TODO находит два патерна
    # def test_invitation_detail(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
    #     print(self.invitation1.id)
    #     response = self.client.get(reverse('invitation_detail'), kwargs={'pk': self.invitation1.id})
    #     print(response.data)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.status_code, 200)
    ##TODO находит два патерна
    # def test_invitation_accept(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
    #     data = {
    #         'order_status': 'Approved'
    #     }
    #     response = self.client.put(reverse('invitation_detail'), kwargs={'pk': self.invitation1}, data=data, format='json')
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.status_code, 200)
    ##TODO находит два патерна
    # def test_invitation_accept_invalid(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
    #     data = {
    #         'order_status': 'Approved'
    #     }
    #     response = self.client.put(reverse('invitation_detail'), kwargs={'pk': self.invitation1}, data=data, format='json')
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.status_code, 403)

 ##TODO на url два патерна
    # def test_post_list(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
    #     post = Post.objects.create(
    #         text='test',
    #         team=self.team1,
    #         user=self.profile1
    #     )
    #     response = self.client.get(reverse('post'), kwargs={'pk': self.team1.id, 'post_pk': post.id})
    #     print(response)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.status_code, 200)

#     def test_post_list_invalid(self):
#         self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
#         post = Post.objects.create(
#             text='test',
#             team=self.team1,
#             user=self.profile2
#         )
#         response = self.client.get(reverse('post'), kwargs={'pk': self.team1.id, 'post_pk': post.id})
#         print(response)
#         self.assertEqual(response.status_code, 403)

    # def test_post_list_invalid(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
    #     response = self.client.get(reverse('post'), kwargs={'pk': self.team1.id})
    #     print(response)
    #     self.assertEqual(response.status_code, 403)

    # def test_post_list_create(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
    #     response = self.client.get(reverse('post'), kwargs={'pk': self.team1.id})
    #     print(response)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.status_code, 200)

    ##TODO на url два патерна
    # def test_member_list(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
    #     response = self.client.get(reverse('member'), kwargs={'pk': self.team1.id})
    #     print(response)
        #     self.assertEqual(len(response.data), 1)
        #     self.assertEqual(response.status_code, 200)

