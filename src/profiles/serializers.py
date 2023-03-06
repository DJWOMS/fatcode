from djoser.serializers import UserSerializer, UserCreatePasswordRetypeSerializer
from djoser.conf import settings
from rest_framework import serializers

from src.base import exceptions

from src.profiles import models, services
from src.profiles.services import add_friend


class UserUpdateSerializer(UserSerializer):
    """Serialization to change user data"""

    class Meta:
        model = models.FatUser
        fields = tuple(models.FatUser.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'first_name',
            'last_name',
            'middle_name'
        )
        read_only_fields = (settings.LOGIN_FIELD,)


class UsersCreateSerializer(UserCreatePasswordRetypeSerializer):
    """Serialization to create user data"""
    email = serializers.EmailField(required=True)
    invite = serializers.CharField(max_length=50)

    class Meta:
        model = models.FatUser
        fields = ('username', 'email', 'password', 'invite')

    def validate(self, attrs):
        self.fields.pop("invite", None)
        invite = attrs.pop('invite')
        services.check_email(attrs.get('email'))
        services.check_invite(invite)
        attrs = super().validate(attrs)
        if attrs:
            services.delete_invite(invite)
            return attrs
        raise exceptions.AuthExists()


class GetUserSerializer(serializers.ModelSerializer):
    """Serialization for other serializers"""

    class Meta:
        model = models.FatUser
        fields = ("id", "username", "avatar")


class GetUserForProjectSerializer(serializers.ModelSerializer):
    """Serialization for other serializers"""

    class Meta:
        model = models.FatUser
        fields = ("id", "username")


class DashboardUserSerializer(serializers.ModelSerializer):
    """Serializer for dashboard"""
    started_courses_count = serializers.SerializerMethodField()
    finished_courses_count = serializers.SerializerMethodField()

    class Meta:
        model = models.FatUser
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


class GitHubAddSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=25)


class AccountsSerializer(serializers.ModelSerializer):
    """Сериализатор аккаунтов пользователя"""

    class Meta:
        model = models.Account
        fields = ('provider', 'account_url')


class SocialsSerializer(serializers.ModelSerializer):
    """Сериализатор социальных ссылок пользователя"""

    class Meta:
        model = models.FatUserSocial
        fields = ('full_social_link', )


class LanguagesSerializer(serializers.ModelSerializer):
    """Сериализатор языков"""

    class Meta:
        model = models.Language
        fields = ('name',)


class UserFieldsSerializer(serializers.ModelSerializer):
    """Сериализатор информации пользователя для анкеты"""

    class Meta:
        model = models.FatUser
        fields = ('username', 'full_name', 'email')


class ApplicationListSerializer(serializers.ModelSerializer):
    getter = GetUserSerializer()

    class Meta:
        model = models.Application
        fields = ('id', 'getter',)


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Application
        fields = ('id', 'getter',)


class FriendListSerializer(serializers.ModelSerializer):
    friend = GetUserSerializer()

    class Meta:
        model = models.Friend
        fields = ('id', 'friend',)

    def create(self, validated_data):
        return add_friend(friend=validated_data['friend'], user=validated_data['user'])


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Friend
        fields = ('id', 'friend',)

    def create(self, validated_data):
        return add_friend(friend=validated_data['friend'], user=validated_data['user'])


class AvatarProfileSerializer(serializers.ModelSerializer):
    """Сериализатор аватара профиля"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUser
        fields = ('avatar', 'user')

    def update(self, instance, validated_data):
        if instance.avatar:
            instance.avatar.delete()
        instance.avatar = validated_data.get('avatar', None)
        instance.save()
        return instance


class SocialProfileSerializer(serializers.ModelSerializer):
    """Просмотр социальных ссылок профиля"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUserSocial
        fields = ('id', 'full_social_link', 'user')


class SocialProfileCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания социальных ссылок профиля"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUserSocial
        fields = ('id', 'social', 'user', 'user_url')

    def create(self, validated_data):
        user = validated_data.pop('user')
        social_link = validated_data.pop('social')
        user_url = validated_data.pop('user_url')
        return services.create_social(user, social_link, user_url)


class SocialProfileUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор обновления социальных ссылок профиля"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUserSocial
        fields = ('id', 'user', 'user_url')

    def update(self, instance, validated_data):
        user_url = validated_data.pop('user_url')
        return services.check_or_update_social(instance, user_url)


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор представления профиля """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_social = SocialProfileSerializer(many=True)

    class Meta:
        model = models.FatUser
        fields = ('id', 'username', 'avatar', 'full_name', 'email', 'user', 'user_social')


class UserProfileListSerializer(serializers.ModelSerializer):
    """Сериализатор представления пользователей """

    class Meta:
        model = models.FatUser
        fields = ('id', 'username', 'avatar', 'full_name', 'email')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор RUDE профиля"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUser
        fields = ('id', 'middle_name', 'email', 'town', 'user')

    def update(self, instance, validated_data):
        email = validated_data.pop('email', None)
        pk = validated_data.pop('pk')
        middle_name = validated_data.pop('middle_name', None)
        town = validated_data.pop('town', None)
        return services.check_or_update_email(instance, email, pk, middle_name, town)


class UserMeProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля для user_me"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUser
        fields = ('id', 'username', 'avatar', 'full_name', 'email', 'user', 'town', 'experience', 'coins')


class SocialListSerializer(serializers.ModelSerializer):
    """Сериализатор социальных сетей"""

    class Meta:
        model = models.Social
        fields = ('title', 'logo', 'url')

