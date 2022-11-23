from django.core.validators import FileExtensionValidator
from django.db import models

from src.base.validators import ImageValidator


class Category(models.Model):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name="children", blank=True, null=True)

    def __str__(self):
        return self.name


class Toolkit(models.Model):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name="children", blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('profiles.FatUser', on_delete=models.CASCADE, related_name="projects")
    category = models.ForeignKey(Category, related_name="projects", on_delete=models.PROTECT, default='1')
    toolkit = models.ManyToManyField(Toolkit, related_name="projects")
    teams = models.ManyToManyField('team.Team', related_name='project_teams')
    avatar = models.ImageField(
        upload_to='project/avatar/',
        default='default/project.jpg',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg']),
            ImageValidator((250, 250), 524288)
        ]
    )
    repository = models.CharField(max_length=150)
    star = models.PositiveIntegerField(blank=True, null=True)
    fork = models.PositiveIntegerField(blank=True, null=True)
    commit = models.PositiveIntegerField(blank=True, null=True)
    last_commit = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    user = models.ForeignKey('profiles.FatUser', on_delete=models.CASCADE, related_name='project_members')
    project = models.ForeignKey(Project, related_name="members", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.user} is member {self.project} project'
