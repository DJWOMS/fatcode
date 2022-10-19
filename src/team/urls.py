from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

teams = views.TeamView.as_view({
    'get': 'list',
    'post': 'create'
})

detail_teams = views.TeamView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
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
    'get': 'list',
})

teams_member_detail = views.MemberTeamListView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
urlpatterns = format_suffix_patterns([
    path('teams/', teams, name='teams'),
    path('teams/<int:pk>/', detail_teams, name='detail_teams'),
    path('own_teams/', teams_owns, name='teams_owns'),
    path('own_teams/<int:pk>/', teams_owns_detail, name='teams_owns_detail'),
    path('teams_member/', teams_member, name='teams_member'),
    path('teams_member/<int:pk>', teams_member_detail, name='teams_member_detail')
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
