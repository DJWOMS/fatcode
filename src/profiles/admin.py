from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from src.profiles import models
from django.utils.translation import gettext_lazy as _
from src.courses.models import UserCourseThrough


class SocialInLineFatUser(admin.TabularInline):
    model = models.FatUser.socials.through


class CourseInLineFatUser(admin.TabularInline):
    model = UserCourseThrough


class FatUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("avatar", "first_name", "last_name",
                                         "middle_name", "email")}),
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
        (_("Important dates"), {"fields": ("last_login", "date_joined", "first_login")}),
        # (_("socials"), {"fields": ("socials", )}),
    )

    inlines = (SocialInLineFatUser, CourseInLineFatUser)


admin.site.register(models.FatUser, FatUserAdmin)
admin.site.register(models.Social)
