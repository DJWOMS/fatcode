from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from src.profiles.models import FatUser
from src.team.models import Post, Comment, Team, TeamMember, Invitation, SocialLink


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
        self.social_link = SocialLink.objects.create(
            name='test',
            link='http://test',
            team=self.team1
        )
        self.comment1 = Comment.objects.create(
            user=self.profile1,
            post=self.post1,
            text='text1',
        )

    def test_team_create_no_authorization(self):
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
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_team_list_no_authorization(self):
        response = self.client.get(reverse('teams'))
        self.assertEqual(len(response.data), 4)
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

    def test_team_update_no_authorization(self):
        data = {
            'name': 'test',
            'user': self.profile4.id
        }
        response = self.client.post(reverse('detail_teams', kwargs={'pk': self.team1.id}), data=data, format='json')
        self.assertEqual(response.status_code, 405)

    def test_team_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.delete(reverse('detail_teams', kwargs={'pk': self.team1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.filter(id=self.team1.id).exists(), False)

    def test_team_delete_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.delete(reverse('detail_teams', kwargs={'pk': self.team1.id}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Team.objects.filter(id=self.team1.id).exists(), True)

    def test_team_delete_no_authorization(self):
        response = self.client.delete(reverse('detail_teams', kwargs={'pk': self.team1.id}))
        self.assertEqual(response.status_code, 401)

    def test_team_detail_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('detail_teams', kwargs={'pk': 500}))
        self.assertEqual(response.status_code, 404)

    def test_my_team(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('my_team'))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_my_team_no_authorization(self):
        response = self.client.get(reverse('my_team'))
        self.assertEqual(response.status_code, 401)

    def test_member_team(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.get(reverse('team_member'))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_member_team_no_authorization(self):
        response = self.client.get(reverse('team_member'))
        self.assertEqual(response.status_code, 401)

    def test_invitation_create(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'team': self.team1.id,
            'user': self.profile2.id
        }
        response = self.client.post(reverse('invitation'), data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(Invitation.objects.count(), 2)

    def test_invitation_create_no_authorization(self):
        data = {
            'team': self.team1.id,
            'user': self.profile4.id
        }
        response = self.client.post(reverse('invitation'), data=data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_invitation_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'team': self.team1.id,
            'user': self.profile1.id
        }
        response = self.client.post(reverse('invitation'), data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(Invitation.objects.count(), 1)

    def test_my_invitation_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.get(reverse('invitation'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(Invitation.objects.count(), 1)

    def test_invitation_no_authorization(self):
        response = self.client.get(reverse('invitation'))
        self.assertEqual(response.status_code, 401)

    def test_invitation_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.get(reverse('invitation_delete', kwargs={'pk': self.invitation.id}))
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.status_code, 200)

    def test_invitation_detail_no_authorization(self):
        response = self.client.get(reverse('invitation_delete', kwargs={'pk': self.invitation.id}))
        self.assertEqual(response.status_code, 401)

    def test_invitation_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.delete(reverse('invitation_delete', kwargs={'pk': self.invitation.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invitation.objects.filter(id=self.invitation.id).exists(), False)

    def test_invitation_delete_no_authorization(self):
        response = self.client.delete('invitation_delete', kwargs={'pk': self.invitation.id})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Invitation.objects.filter(id=self.invitation.id).exists(), True)

    def test_invitation_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('invitation_list'))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_invitation_list_no_authorization(self):
        response = self.client.get(reverse('invitation_list'))
        self.assertEqual(response.status_code, 401)

    def test_invitation_list_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('invitation_detail', kwargs={'pk': self.invitation.id}))
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.status_code, 200)

    def test_invitation_list_detail_no_authorization(self):
        response = self.client.post(reverse('invitation_detail', kwargs={'pk': self.invitation.id}))
        self.assertEqual(response.status_code, 405)

    def test_invitation_update_approved(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'order_status': 'Approved',
            'user': self.profile1.id
        }
        response = self.client.put(reverse('invitation_detail',
                                           kwargs={'pk': self.invitation.id}), data=data, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_invitation_update_rejected(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'order_status': 'Rejected',
            'user': self.profile1.id
        }
        response = self.client.put(reverse('invitation_detail',
                                           kwargs={'pk': self.invitation.id}), data=data, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_post_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('post', kwargs={'pk': self.team1.id}))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_post_list_member(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.get(reverse('post', kwargs={'pk': self.team1.id}))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_post_list_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.get(reverse('post', kwargs={'pk': self.team1.id}))
        self.assertEqual(response.status_code, 403)

    def test_post_create(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'text': 'test',
            'user': self.profile1.id,
            'team': self.team1.id
        }
        response = self.client.post(reverse('post', kwargs={'pk': self.team1.id}), data=data, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 201)

    def test_post_create_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'text': 'test',
            'user': self.profile2.id,
            'team': self.team1.id
        }
        response = self.client.post(reverse('post', kwargs={'pk': self.team1.id}), data=data, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_post_author_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('update_or_delete_post',
                                           kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}))
        self.assertEqual(len(response.data), 6)
        self.assertEqual(response.status_code, 200)

    def test_post_member_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.get(reverse('update_or_delete_post',
                                           kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}))
        self.assertEqual(len(response.data), 6)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.get(reverse('update_or_delete_post',
                                           kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_post_author_update(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'text': 'test',
            'user': self.profile1.id,
            'team': self.team1.id
        }
        response = self.client.put(reverse('update_or_delete_post',
                                           kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}),
                                   data=data, format='json'
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_post_member_update_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        data = {
            'text': 'test',
            'user': self.profile3.id,
            'team': self.team1.id
        }
        response = self.client.put(reverse('update_or_delete_post',
                                           kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}),
                                   data=data, format='json'
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_post_update_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'text': 'test',
            'user': self.profile2.id,
            'team': self.team1.id
        }
        response = self.client.put(reverse('update_or_delete_post',
                                           kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}),
                                   data=data, format='json'
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_post_author_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.delete(reverse('update_or_delete_post',
                                           kwargs={'pk': self.team1.id, 'post_pk': self.post1.id})
                                   )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.filter(id=self.post1.id).exists(), False)

    def test_post_member_delete_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.delete(reverse('update_or_delete_post',
                                           kwargs={'pk': self.team1.id, 'post_pk': self.post1.id})
                                   )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Post.objects.filter(id=self.post1.id).exists(), True)

    def test_post_delete_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.delete(reverse('update_or_delete_post',
                                           kwargs={'pk': self.team1.id, 'post_pk': self.post1.id})
                                   )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Post.objects.exists(), True)

    def test_comment_author_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('comment', kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_comment_member_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.get(reverse('comment', kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_comment_list_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.get(reverse('comment', kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_comment_create(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'text': 'test_1',
            'user': self.profile1.id,
            'post': self.post1.id
        }
        response = self.client.post(reverse('comment',
                                            kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}),
                                    data=data, format='json'
                                    )
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, 201)

    def test_comment_member_create(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        data = {
            'text': 'test_1',
            'user': self.profile3.id,
            'post': self.post1.id
        }
        response = self.client.post(reverse('comment',
                                            kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}),
                                    data=data, format='json'
                                    )
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, 201)

    def test_comment_create_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'text': 'test_1',
            'user': self.profile2.id,
            'post': self.post1.id
        }
        response = self.client.post(reverse('comment',
                                            kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}),
                                    data=data, format='json'
                                    )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_comment_parent_create(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'text': 'test_1',
            'user': self.profile1.id,
            'post': self.post1.id,
            'parent': self.comment1.id
        }
        response = self.client.post(reverse('comment',
                                            kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}),
                                    data=data, format='json'
                                    )
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, 201)

    def test_comment_parent_create_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'text': 'test_1',
            'user': self.profile2.id,
            'post': self.post1.id,
            'parent': self.comment1.id
        }
        response = self.client.post(reverse('comment',
                                            kwargs={'pk': self.team1.id, 'post_pk': self.post1.id}),
                                    data=data, format='json'
                                    )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_comment_author_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('comment_detail',
                                            kwargs={'pk': self.team1.id,
                                                    'post_pk': self.post1.id,
                                                    'comment_pk': self.comment1.id})
                                    )
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.status_code, 200)

    def test_comment_member_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.get(reverse('comment_detail',
                                            kwargs={'pk': self.team1.id,
                                                    'post_pk': self.post1.id,
                                                    'comment_pk': self.comment1.id})
                                    )
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.status_code, 200)

    def test_comment_retrieve_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.get(reverse('comment_detail',
                                            kwargs={'pk': self.team1.id,
                                                    'post_pk': self.post1.id,
                                                    'comment_pk': self.comment1.id})
                                    )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_comment_author_update(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'text': 'test_1',
            'user': self.profile1.id,
            'post': self.post1.id
        }
        response = self.client.put(reverse('comment_detail',
                                            kwargs={'pk': self.team1.id,
                                                    'post_pk': self.post1.id,
                                                    'comment_pk': self.comment1.id}),
                                    data=data, format='json'
                                    )
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_comment_member_update_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        data = {
            'text': 'test_1',
            'user': self.profile3.id,
            'post': self.post1.id
        }
        response = self.client.put(reverse('comment_detail',
                                            kwargs={'pk': self.team1.id,
                                                    'post_pk': self.post1.id,
                                                    'comment_pk': self.comment1.id}),
                                    data=data, format='json'
                                    )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_comment_update_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'text': 'test_1',
            'user': self.profile2.id,
            'post': self.post1.id
        }
        response = self.client.put(reverse('comment_detail',
                                            kwargs={'pk': self.team1.id,
                                                    'post_pk': self.post1.id,
                                                    'comment_pk': self.comment1.id}),
                                    data=data, format='json'
                                    )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_comment_author_parent_update(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'text': 'test_1',
            'user': self.profile1.id,
            'post': self.post1.id,
            'parent': self.comment1.id
        }
        response = self.client.put(reverse('comment_detail',
                                            kwargs={'pk': self.team1.id,
                                                    'post_pk': self.post1.id,
                                                    'comment_pk': self.comment1.id}),
                                    data=data, format='json'
                                    )
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_comment_member_parent_update_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        data = {
            'text': 'test_1',
            'user': self.profile3.id,
            'post': self.post1.id,
            'parent': self.comment1.id
        }
        response = self.client.put(reverse('comment_detail',
                                            kwargs={'pk': self.team1.id,
                                                    'post_pk': self.post1.id,
                                                    'comment_pk': self.comment1.id}),
                                    data=data, format='json'
                                    )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_comment_parent_update_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        data = {
            'text': 'test_1',
            'user': self.profile2.id,
            'post': self.post1.id,
            'parent': self.comment1.id
        }
        response = self.client.put(reverse('comment_detail',
                                            kwargs={'pk': self.team1.id,
                                                    'post_pk': self.post1.id,
                                                    'comment_pk': self.comment1.id}),
                                    data=data, format='json'
                                    )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_comment_author_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.delete(reverse('comment_detail',
                                            kwargs={'pk': self.team1.id,
                                                    'post_pk': self.post1.id,
                                                    'comment_pk': self.comment1.id})
                                      )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.filter(id=self.comment1.id).exists(), False)

    def test_comment_member_delete_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.delete(reverse('comment_detail',
                                            kwargs={'pk': self.team1.id,
                                                    'post_pk': self.post1.id,
                                                    'comment_pk': self.comment1.id})
                                      )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Comment.objects.filter(id=self.comment1.id).exists(), True)

    def test_comment_delete_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.delete(reverse('comment_detail',
                                            kwargs={'pk': self.team1.id,
                                                    'post_pk': self.post1.id,
                                                    'comment_pk': self.comment1.id})
                                      )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Comment.objects.filter(id=self.comment1.id).exists(), True)

    def test_member_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.get(reverse('member', kwargs={'pk': self.team1.id}))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_member_list_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.get(reverse('member', kwargs={'pk': self.team1.id}))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_member_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('member_detail',
                                           kwargs={'pk': self.team1.id, 'member_pk': self.team_member1.id})
                                   )
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_member_retrieve_member(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.get(reverse('member_detail',
                                           kwargs={'pk': self.team1.id, 'member_pk': self.team_member1.id})
                                   )
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_member_retrieve_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.get(reverse('member_detail',
                                           kwargs={'pk': self.team1.id, 'member_pk': self.team_member1.id})
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_member_author_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.delete(reverse('member_detail',
                                           kwargs={'pk': self.team1.id, 'member_pk': self.team_member1.id})
                                      )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TeamMember.objects.filter(id=self.team_member1.id).exists(), False)

    def test_member_delete_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile2_token.key)
        response = self.client.delete(reverse('member_detail',
                                           kwargs={'pk': self.team1.id, 'member_pk': self.team_member1.id})
                                      )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(TeamMember.objects.filter(id=self.team_member1.id).exists(), True)

    def test_member_member_team_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.delete(reverse('member_detail',
                                           kwargs={'pk': self.team1.id, 'member_pk': self.team_member1.id})
                                      )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(TeamMember.objects.filter(id=self.team_member1.id).exists(), True)

    def test_social_links_list(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('social_links', kwargs={'pk': self.team1.id}))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_social_links_list_no_authorization(self):
        response = self.client.get(reverse('social_links', kwargs={'pk': self.team1.id}))
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_social_links_create(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'test_2',
            'link': 'https://test.com/',
            'team': self.team1.id
        }
        response = self.client.post(reverse('social_links', kwargs={'pk': self.team1.id}), data=data, format='json')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 201)

    def test_social_links_create_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        data = {
            'name': 'test_3',
            'link': 'https://test.com/',
            'team': self.team1.id
        }
        response = self.client.post(reverse('social_links', kwargs={'pk': self.team1.id}), data=data, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_social_links_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.get(reverse('social_link_detail',
                                           kwargs={'pk': self.team1.id, 'social_pk': self.social_link.id})
                                   )
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, 200)

    def test_social_links_update(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        data = {
            'name': 'test_3',
            'link': 'https://test.com/',
            'team': self.team1.id
        }
        response = self.client.put(reverse('social_link_detail',
                                           kwargs={'pk': self.team1.id, 'social_pk': self.social_link.id}),
                                   data=data, format='json'
                                   )
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_social_links_update_invalide(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        data = {
            'name': 'test_4',
            'link': 'https://test.com/',
            'team': self.team1.id
        }
        response = self.client.put(reverse('social_link_detail',
                                           kwargs={'pk': self.team1.id, 'social_pk': self.social_link.id}),
                                   data=data, format='json'
                                   )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 403)

    def test_social_links_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile1_token.key)
        response = self.client.delete(reverse('social_link_detail',
                                           kwargs={'pk': self.team1.id, 'social_pk': self.social_link.id})
                                   )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SocialLink.objects.filter(id=self.social_link.id).exists(), False)

    def test_social_links_delete_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.profile3_token.key)
        response = self.client.delete(reverse('social_link_detail',
                                           kwargs={'pk': self.team1.id, 'social_pk': self.social_link.id})
                                   )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(SocialLink.objects.filter(id=self.social_link.id).exists(), True)
