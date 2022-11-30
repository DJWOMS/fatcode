from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import uuid

from django.http import HttpResponseRedirect
from src.profiles import models
from django.utils.translation import gettext_lazy as _
from src.courses.models import UserCourseThrough
from django.urls import path


class SocialInLineFatUser(admin.TabularInline):
    model = models.FatUser.socials.through


class CourseInLineFatUser(admin.TabularInline):
    model = UserCourseThrough


class FatUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("avatar", "first_name", "last_name",
                                         "middle_name", "email", "coins")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        # (_("socials"), {"fields": ("socials", )}),
    )

    inlines = (SocialInLineFatUser, CourseInLineFatUser)


class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "account_id", "account_url", "account_name")
    search_fields = ("user", "account_id", "account_url", "account_name")


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('user', 'description')
    search_fields = ('user', )


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


class FatUserSocialAdmin(admin.ModelAdmin):
    list_display = ('social', 'user', 'user_url')


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('code', )
    change_list_template = "admin/invite.html"

    def get_urls(self):
        urls = super(InvitationAdmin, self).get_urls()
        custom_urls = [
            path('make_invitation/', self.make_invitation, name='make_invitation'), ]
        return custom_urls + urls

    def make_invitation(self, request):
        for item in range(11):
            item = uuid.uuid4()
            models.Invitation.objects.create(code=item)
        return HttpResponseRedirect("../")


admin.site.register(models.FatUser, FatUserAdmin)
admin.site.register(models.Social)
admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.Questionnaire, QuestionnaireAdmin)
admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.FatUserSocial, FatUserSocialAdmin)
admin.site.register(models.Applications)
admin.site.register(models.Friends)
admin.site.register(models.Invitation, InvitationAdmin)

