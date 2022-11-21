from datetime import datetime

from djoser.serializers import UserSerializer
from djoser.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from src.courses.serializers import ListCourseSerializer
from src.profiles import models
from src.base.validators import ImageValidator
from django.db.models import Sum, Count, Q

from src.profiles.services import add_friend


class UserUpdateSerializer(UserSerializer):
    """Serialization to change user data"""

    class Meta:
        model = FatUser
        fields = tuple(FatUser.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'first_name',
            'last_name',
            'middle_name'
        )
        read_only_fields = (settings.LOGIN_FIELD,)


class UserSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatUserSocial
        fields = '__all__'


class ListSocialSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(read_only=True)

    class Meta:
        model = Social
        fields = '__all__'


class UserAvatarSerializer(serializers.ModelSerializer):
    """Update user avatar"""
    avatar = serializers.ImageField(validators=[ImageValidator((100, 100), 1048576)])

    class Meta:
        model = FatUser
        fields = [
            "id",
            "avatar"
        ]


class AccountSerializer(serializers.ModelSerializer):
    """Serialization for user's git_hub account"""

    class Meta:
        model = Account
        fields = ("url", )

#TODO не выводяться аккаунты гита
class UserSerializer(serializers.ModelSerializer):
    """Serialization for user's internal display"""
    email = serializers.EmailField(read_only=True)
    avatar = serializers.ImageField(validators=[ImageValidator((100, 100), 1048576)])
    user_social = UserSocialSerializer(many=True)
    socials = ListSocialSerializer(many=True)
    courses = ListCourseSerializer(many=True)
    user_account = AccountSerializer(read_only=True)

    class Meta:
        model = FatUser
        exclude = (
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions"
        )
        ref_name = "Fat user"

    def update(self, instance, validated_data):
        if validated_data.get('user_social', None):
            user_social = validated_data.pop('user_social')
            self.update_user_social(instance, user_social)

        return super().update(instance, validated_data)

    def update_user_social(self, instance, user_social):
        for soc in user_social:
            entry_fatUserSocial = instance.user_social.filter(
                social=soc['social']).first()

            if entry_fatUserSocial is not None:
                entry_fatUserSocial.user_url = soc['user_url']
                entry_fatUserSocial.save()
            else:
                instance.user_social.create(social=soc['social'], user_url=soc['user_url'])


class UserPublicSerializer(serializers.ModelSerializer):
    """Serialization for public user display"""

    avatar = serializers.ImageField(read_only=True)
    user_social = UserSocialSerializer(many=True)
    socials = ListSocialSerializer(many=True)
    courses = ListCourseSerializer(many=True)

    class Meta:
        model = FatUser
        exclude = (
            "email",
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


class GetUserSerializer(serializers.ModelSerializer):
    """Serialization for other serializers"""

    class Meta:
        model = FatUser
        fields = ("id", "username", "avatar")


class DashboardUserSerializer(serializers.ModelSerializer):
    """Serializer for dashboard"""
    started_courses_count = serializers.SerializerMethodField()
    finished_courses_count = serializers.SerializerMethodField()

    class Meta:
        model = FatUser
        fields = (
                'coins',
                'experience',
                'username',
                'id',
                'started_courses_count',
                'finished_courses_count'
            )

        def get_started_courses_count(self, instance):
            return instance.courses.filter(progress=0).count()

        def get_finished_courses_count(self, instance):
            return instance.courses.filter(progress=100).count()


class GitHubLoginSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=150)


class GitHubAddSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=25)


class ApplicationListSerializer(serializers.ModelSerializer):
    getter = GetUserSerializer()

    class Meta:
        model = models.Applications
        fields = ('id', 'getter', )


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Applications
        fields = ('id', 'getter', )


class FriendListSerializer(serializers.ModelSerializer):
    friend = GetUserSerializer()

    class Meta:
        model = models.Friends
        fields = ('id', 'friend', )

    def create(self, validated_data):
        return add_friend(friend=validated_data['friend'], user=validated_data['user'])


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Friends
        fields = ('id', 'friend', )

    def create(self, validated_data):
        return add_friend(friend=validated_data['friend'], user=validated_data['user'])