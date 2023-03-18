import pytz

from django.db import models
from django.core.validators import FileExtensionValidator

from src.base.validators import ImageValidator
from .validators import phone_validator, birthday_validator
from src.profiles.models import FatUser, Account, FatUserSocial, Language


class Questionnaire(models.Model):
    """Модель анкеты"""
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    description = models.TextField()
    country = models.CharField(max_length=150, blank=True, null=True)
    town = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(validators=[phone_validator], max_length=13, blank=True, null=True)
    birthday = models.DateField(validators=[birthday_validator], blank=True, null=True)
    avatar = models.ImageField(
        upload_to='questionnaire/avatar/',
        default='default/default.jpg',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg']),
            ImageValidator((250, 250), 524288)
        ]
    )
    timezone = models.CharField(max_length=32, choices=TIMEZONES,
                                default='UTC')
    user = models.OneToOneField(FatUser, on_delete=models.CASCADE, related_name='questionnaire')
    toolkits = models.ManyToManyField(
        'repository.Toolkit',
        related_name="questionnaire_projects",
        blank=True
    )
    teams = models.ManyToManyField('team.Team', related_name='questionnaire_teams', blank=True)
    projects = models.ManyToManyField(
        'repository.Project',
        related_name='questionnaire_projects',
        blank=True
    )
    accounts = models.ManyToManyField(Account, related_name='questionnaire_accounts', blank=True)
    languages = models.ManyToManyField(Language, related_name="questionnaire_language", blank=True)
    socials = models.ManyToManyField(FatUserSocial, related_name="questionnaire_social", blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.id}'


