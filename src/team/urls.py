from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

teams = views.TeamView.as_view({
    'get': 'list',
    'post': 'create'
})

detail_teams = views.TeamView.as_view({
    'get': 'retrieve',
})

teams_owns = views.OwnTeamListView.as_view({
    'get': 'list',
})

teams_owns_detail = views.OwnTeamListView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

teams_member = views.MemberTeamListView.as_view({
    'get': 'list'
})

teams_member_detail = views.MemberTeamListView.as_view({
    'get': 'retrieve'
})

add_post = views.PostView.as_view({
    'post': 'create'
})

posts = views.PostView.as_view({
    'get': 'list',
    'post': 'create'
})

update_or_delete_post = views.PostView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
comments = views.CommentsView.as_view({
    'get': 'list',
    'post': 'create'
})

comment_detail = views.CommentsView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

invitation = views.InvitationView.as_view({
    'get': 'list',
    'post': 'create'
})

invitation_delete = views.InvitationView.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

invitation_list = views.InvitationDetailView.as_view({
    'get': 'list'
})

invitation_detail = views.InvitationDetailView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
urlpatterns = format_suffix_patterns([
    path('teams/', teams, name='teams'),
    path('teams/<int:pk>/', detail_teams, name='detail_teams'),
    path('own_teams/', teams_owns, name='teams_owns'),
    path('own_teams/<int:pk>/', teams_owns_detail, name='teams_owns_detail'),
    path('own_teams/<int:pk>/add_post', add_post, name='add_post'),
    path('teams_member/', teams_member, name='teams_member'),
    path('teams_member/<int:pk>/', teams_member_detail, name='teams_member_detail'),
    path('posts/', posts, name='post'),
    path('posts/<int:pk>/', update_or_delete_post, name='update_or_delete_post'),
    path('comments/', comments, name='comments'),
    path('comments/<int:pk>', comment_detail, name='comment_detail'),
    path('invitation/', invitation, name='invitation'),
    path('invitation/<int:pk>/', invitation_delete, name='invitation_delete'),
    path('invitation_list/', invitation_list, name='invitation_list'),
    path('invitation_list/<int:pk>/', invitation_detail, name='invitation_detail'),
])

#
# urlpatterns = [
#     path('invitation/', views.InvitationCreateView.as_view()),
#     path('invitation/answer/list/', views.InvitationAskingListView.as_view()),
#     path('invitation/answer/', views.InvitationAskingView.as_view({'post': 'create'})),
#     path('invitation/answer/<int:pk>/', views.AcceptInvitationAskingView.as_view(
#         {'put': 'update', 'delete': 'destroy'}
#     )),
#
#     path('<int:pk>/member/', views.TeamMemberListView.as_view()),
#     path('member/<int:pk>/', views.TeamMemberView.as_view(
#         {'get': 'retrieve'}
#     )),
#     path('member/<int:team>/retire/', views.TeamMemberSelfDeleteView.as_view(
#         {'delete': 'destroy'}
#     )),
#
#     path('member/<int:pk>/<int:team>/', views.TeamMemberView.as_view(
#         {'delete': 'destroy'}
#     )),
#
#     path('<int:pk>/post/', views.PostListView.as_view()),
#     path('post/', views.PostView.as_view({'post': 'create'})),
#     path('post/<int:pk>/', views.PostView.as_view(
#         {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
#     )),
#
#     path('comment/', views.CommentsView.as_view({'post': 'create'})),
#     path('comment/<int:pk>/', views.CommentsView.as_view({'put': 'update', 'delete': 'destroy'})),
#
#     path('list/', views.TeamListView.as_view()),
#     # path('by_user/<int:pk>/', views.TeamListByUserView.as_view(), name='team_list_by_user'),
#     path('by_user/', views.TeamListByUserView.as_view()),
#
#     path('social_link/', views.SocialLinkView.as_view({'post': 'create'})),
#     path('social_link/<int:pk>/', views.SocialLinkView.as_view(
#         {'put': 'update', 'delete': 'destroy'}
#     )),
#
#     path('<int:pk>/avatar/', views.TeamAvatarView.as_view({'put': 'update'})),
#     path('<int:pk>/', views.TeamView.as_view(
#         {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
#     )),
#     path('', views.TeamView.as_view({'post': 'create'}))
# ]
