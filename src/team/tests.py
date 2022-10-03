from django.urls import reverse
from rest_framework.test import APITestCase

from src.profiles.models import FatUser
from src.team.models import Post, Comment, Team, TeamMember, Invitation


class TeamTest(APITestCase):
    def setUp(self):
        self.profile1 = FatUser.objects.create(
            username='username1',
            phone='45675',
            avatar=None
        )
        self.profile2 = FatUser.objects.create(
            username='username2',
            phone='68679t',
        )
        self.profile3 = FatUser.objects.create(
            username='username3',
            phone='0773535',
        )
        self.profile4 = FatUser.objects.create(
            username='username4',
            phone='0773535',
        )

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

        self.invitation1 = Invitation.objects.create(
            team=self.team3,
            user=self.profile1,
            asking=False
        )
        self.invitation_asking1 = Invitation.objects.create(
            team=self.team1,
            user=self.profile3,
            asking=True
        )

        self.post1 = Post.objects.create(
            text='text1',
            user=self.profile1,
            team=self.team1
        )
        self.post2 = Post.objects.create(
            text='text2',
            user=self.profile3,
            team=self.team1
        )
        self.comment1 = Comment.objects.create(
            user=self.profile1,
            post=self.post1,
            text='text1',
        )
        self.comment2 = Comment.objects.create(
            user=self.profile2,
            post=self.post1,
            text='text2',
        )

    def test_team_create_invalid(self):
        response = self.client.post(reverse('team_create'))
        self.assertEqual(response.status_code, 403)

    def test_team_create(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'name': 'name1'
        }
        response = self.client.post(reverse('team_create'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_team_detail(self):
        response = self.client.get(reverse('team_detail', kwargs={'pk': self.team1.id}))
        self.assertEqual(response.status_code, 200)

    def test_team_list(self):
        response = self.client.get(reverse('team_list'))
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, 200)

    def test_invitation_list(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('invitation_list'))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_invitation_asking_list(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('invitation_asking_list'))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_invitation_create_invalid_team_author(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'team': self.team2.id,
            'user': self.profile3.id
        }
        response = self.client.post(reverse('invitation_create'), data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_invitation_create(self):
        self.client.force_authenticate(user=self.profile2)
        data = {
            'team': self.team2.id,
            'user': self.profile3.id
        }
        response = self.client.post(reverse('invitation_create'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_accept_invitation_invalid(self):
        self.client.force_authenticate(user=self.profile2)
        data = {
            'accepted': True
        }
        response = self.client.put(reverse('accept_invitation', kwargs={'pk': self.invitation1.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_accept_self_invitation(self):
        self.client.force_authenticate(user=self.profile3)
        data = {
            'accepted': True
        }
        response = self.client.put(reverse('accept_invitation', kwargs={'pk': self.invitation1.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_accept_invitation(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'accepted': True
        }
        response = self.client.put(reverse('accept_invitation', kwargs={'pk': self.invitation1.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_accept_invitation_asking_invalid(self):
        self.client.force_authenticate(user=self.profile2)
        data = {
            'accepted': True
        }
        response = self.client.put(reverse(
            'accept_invitation_asking', kwargs={'pk': self.invitation_asking1.id}
        ), data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_accept_self_invitation_asking(self):
        self.client.force_authenticate(user=self.profile3)
        data = {
            'accepted': True
        }
        response = self.client.put(reverse(
            'accept_invitation', kwargs={'pk': self.invitation_asking1.id}
        ), data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_accept_asking_invitation(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'accepted': True
        }
        response = self.client.put(reverse(
            'accept_invitation_asking', kwargs={'pk': self.invitation_asking1.id}
        ), data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_team_update_invalid_author(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'name': 'namedfgdfg1'
        }
        response = self.client.put(reverse('team_detail', kwargs={'pk': self.team2.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_invitation_asking_create(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'team': self.team3.id,
        }
        response = self.client.post(reverse('invitation_asking_create'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_team_update(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'name': 'namedfgdfg1'
        }
        response = self.client.put(reverse('team_detail', kwargs={'pk': self.team1.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_team_destroy_invalid_author(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(reverse('team_detail', kwargs={'pk': self.team2.id}))
        self.assertEqual(response.status_code, 403)

    def test_team_destroy(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(reverse('team_detail', kwargs={'pk': self.team3.id}))
        self.assertEqual(response.status_code, 204)

    def test_team_member_list(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('team_member_list', kwargs={'pk': self.team1.id}))
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_team_member_detail(self):
        response = self.client.get(
            reverse('team_member_detail', kwargs={'pk': self.team_member1.id}))
        self.assertEqual(response.status_code, 200)

    def test_team_member_destroy_invalid_author(self):
        self.client.force_authenticate(user=self.profile3)
        response = self.client.delete(reverse('team_member_detail',
                                              kwargs={'pk': self.team_member1.id}))
        self.assertEqual(response.status_code, 403)

    def test_team_member_destroy(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(reverse('team_member_detail',
                                              kwargs={'pk': self.team_member1.id}))
        self.assertEqual(response.status_code, 204)

    def test_comment_create_invalid_team_member(self):
        self.client.force_authenticate(user=self.profile4)
        data = {
            'post': self.post1.id,
            'text': 'hello'
        }
        response = self.client.post(reverse('team_comment_create'), data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_comment_create(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'post': self.post1.id,
            'text': 'hello'
        }
        response = self.client.post(reverse('team_comment_create'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_comment_update_invalid_is_author(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'post': self.post1.id,
            'text': 'goodbye'
        }
        response = self.client.put(reverse('team_comment_detail', kwargs={'pk': self.comment2.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_comment_update(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'post': self.post1.id,
            'text': 'goodbye'
        }
        response = self.client.put(reverse('team_comment_detail', kwargs={'pk': self.comment1.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_comment_destroy_invalid(self):
        response = self.client.delete(reverse('team_comment_detail',
                                              kwargs={'pk': self.comment1.id}))
        self.assertEqual(response.status_code, 403)

    def test_comment_destroy_invalid_is_author(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(reverse('team_comment_detail',
                                              kwargs={'pk': self.comment2.id}))
        self.assertEqual(response.status_code, 403)

    def test_comment_destroy(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(reverse('team_comment_detail',
                                              kwargs={'pk': self.comment1.id}))
        self.assertEqual(response.status_code, 204)

    def test_post_create_invalid_team_member(self):
        self.client.force_authenticate(user=self.profile4)
        data = {
            'team': self.team1.id,
            'text': 'text3'
        }
        response = self.client.post(reverse('team_post_create'), data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_post_create(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'team': self.team1.id,
            'text': 'text3',
        }
        response = self.client.post(reverse('team_post_create'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_post_detail_invalid_team_member(self):
        self.client.force_authenticate(user=self.profile4)
        response = self.client.get(reverse('team_post_detail', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, 403)

    def test_post_detail(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.get(reverse('team_post_detail', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_update_invalid_is_author(self):
        self.client.force_authenticate(user=self.profile2)
        data = {
            'post': self.post1.id,
            'text': 'goodbye',
            'team': self.team1.id

        }
        response = self.client.put(reverse('team_post_detail', kwargs={'pk': self.post2.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_post_update(self):
        self.client.force_authenticate(user=self.profile1)
        data = {
            'post': self.post1.id,
            'text': 'goodbye',
            'team': self.team1.id
        }
        response = self.client.put(reverse('team_post_detail', kwargs={'pk': self.post1.id}),
                                   data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_post_destroy_invalid_is_author(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(reverse('team_post_detail', kwargs={'pk': self.post2.id}))
        self.assertEqual(response.status_code, 403)

    def test_post_destroy(self):
        self.client.force_authenticate(user=self.profile1)
        response = self.client.delete(reverse('team_post_detail', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, 204)
