from django.contrib import admin

from src.team import models


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "id")
    search_fields = ("name", "user__username")


@admin.register(models.Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("user", "team", "id")
    search_fields = ("user__username", "team__name")


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "user", "published", "create_date", "moderation", "view_count")


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "create_date", "update_date", "is_publish", "is_delete", "id")


@admin.register(models.TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "team", "id")
    search_fields = ("user__username", "team__name")


@admin.register(models.SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "id")
