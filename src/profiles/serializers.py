from djoser.serializers import UserSerializer, UserCreatePasswordRetypeSerializer
from djoser.conf import settings
from rest_framework.validators import UniqueValidator
from src.profiles.models import FatUser, Social, FatUserSocial
from rest_framework import serializers
from src.profiles.validators import AvatarValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from datetime import datetime
from src.courses.serializers import ListCourseSerializer


class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    """Serialization to create user"""

    email = serializers.EmailField(
        required=True,
        max_length=100,
        validators=[
           UniqueValidator(
               queryset=FatUser.objects.all(),
               message='Такой email уже используется',
           )
        ])

    class Meta:
        model = FatUser
        fields = tuple(FatUser.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password",
        )


class UserUpdateSerializer(UserSerializer):
    """Serialization to change user data"""

    email = serializers.EmailField(
        required=True,
        max_length=100,
        validators=[
           UniqueValidator(
               queryset=FatUser.objects.all(),
               message='Такой email уже используется'
           )
        ])

    avatar = serializers.ImageField(validators=[AvatarValidator()])

    class Meta:
        model = FatUser
        fields = tuple(FatUser.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'avatar',
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


class UserSerializer(serializers.ModelSerializer):
    """Serialization for user's internal display"""

    avatar = serializers.ImageField(validators=[AvatarValidator()])
    user_social = UserSocialSerializer(many=True)
    socials = ListSocialSerializer(many=True)
    courses = ListCourseSerializer(many=True)

    class Meta:
        model = FatUser
        exclude = (
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )

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


@receiver(post_save, sender=Token)
def check_first_login(instance: Token, *args, **kwargs):
    """Registration of the first user authorization"""

    user = instance.user
    if user.first_login is None:
        user.first_login = datetime.now()
        user.save()
