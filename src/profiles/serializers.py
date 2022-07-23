from djoser.serializers import UserSerializer, UserCreateSerializer
from djoser.conf import settings
from rest_framework.validators import UniqueValidator
from src.profiles.models import FatUser, Social, FatUserSocial
from rest_framework import serializers
from src.profiles.validators import AvatarValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from datetime import datetime


class FatUserCreateSerializer(UserCreateSerializer):
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


class FatUserUpdateSerializer(UserSerializer):
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


class User_SocialSerializer(serializers.Serializer):
    social_id = serializers.IntegerField()
    social = serializers.CharField(max_length=100)
    user_url = serializers.CharField(max_length=100)


class SocialsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=30)
    logo = serializers.ImageField(read_only=True)


class ListSocialSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(read_only=True)

    class Meta:
        model = Social
        fields = '__all__'


class UserFatSerializer(serializers.ModelSerializer):
    """Serialization for user's internal display"""

    avatar = serializers.ImageField(validators=[AvatarValidator()])
    user_social = User_SocialSerializer(many=True)
    socials = ListSocialSerializer(many=True)

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


class UserFatPublicSerializer(serializers.ModelSerializer):
    """Serialization for public user display"""

    avatar = serializers.ImageField(read_only=True)

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
            'courses'
        )





@receiver(post_save, sender=Token)
def check_first_login(instance, *args, **kwargs):
    """Registration of the first user authorization"""

    user = instance.user
    if user.first_login is None:
        user.first_login = datetime.now()
        user.save()
