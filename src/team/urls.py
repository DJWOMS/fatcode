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

social_links = views.SocialLinkView.as_view({
    'get': 'list',
    'post': 'create'
})

social_link_detail = views.SocialLinkView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

show_posts = views.ShowPostsView.as_view({
    'get': 'list'
})

show_post = views.ShowPostsView.as_view({
    'get': 'retrieve'
})

show_comments = views.CommentsViewOwn.as_view({
    'get': 'list'
})

show_comment = views.CommentsViewOwn.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    path('teams/', teams, name='teams'),
    path('teams/<int:pk>/', detail_teams, name='detail_teams'),
    path('own_teams/', teams_owns, name='teams_owns'),
    path('own_teams/<int:pk>/', teams_owns_detail, name='teams_owns_detail'),
    path('own_teams/<int:pk>/add_post', add_post, name='add_post'),
    path('members/', teams_member, name='teams_member'),
    path('members/<int:pk>/', teams_member_detail, name='teams_member_detail'),
    path('posts/', posts, name='post'),
    path('posts/<int:pk>/', update_or_delete_post, name='update_or_delete_post'),
    path('show_post/', show_posts, name='show_posts'),
    path('show_post/<int:pk>/', show_post, name='show_post'),
    path('show_comment/', comments, name='comments'),
    path('show_comments/<int:pk>/', comment_detail, name='comment_detail'),
    path('comment/', show_comments, name='show_comments'),
    path('comment/<int:pk>/', show_comment, name='show_comment'),
    path('invitation/', invitation, name='invitation'),
    path('invitation/<int:pk>/', invitation_delete, name='invitation_delete'),
    path('invitation_list/', invitation_list, name='invitation_list'),
    path('invitation_list/<int:pk>/', invitation_detail, name='invitation_detail'),
    path('social_link/', social_links, name='social_links'),
    path('social_link/<int:pk>/', social_link_detail, name='social_link_detail'),
    path('<int:pk>/', detail_teams, name='detail_teams'),
    path('', teams, name='teams'),
])
