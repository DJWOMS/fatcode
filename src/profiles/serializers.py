from djoser.serializers import UserSerializer, UserCreateSerializer
from djoser.conf import settings
from rest_framework.validators import UniqueValidator
from src.profiles.models import FatUser
from rest_framework import serializers
from src.profiles.validators import AvatarValidator


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


class UserFatSerializer(serializers.ModelSerializer):
    """Serialization for user's internal display"""

    avatar = serializers.ImageField(validators=[AvatarValidator()])

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
            "user_permissions"
        )
