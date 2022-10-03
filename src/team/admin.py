from django.contrib import admin

from src.team.models import Post, Comment, Team, TeamMember, Invitation, SocialLink


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "id")
    search_fields = ("name", "user__username")


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("user", "team", "accepted", "asking", "id")
    search_fields = ("user__username", "team__name")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "user", "published", "create_date", "moderation", "view_count")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "create_date", "update_date", "is_publish", "is_delete", "id")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "team", "id")
    search_fields = ("user__username", "team__name")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "id")
