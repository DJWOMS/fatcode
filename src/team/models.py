from django.core.validators import FileExtensionValidator
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from src.profiles.models import FatUser
from src.base.validators import ImageValidator


class Team(models.Model):
    name = models.CharField(max_length=50)
    tagline = models.CharField(max_length=150, null=True, blank=True)
    avatar = models.ImageField(
        upload_to='team/avatar/',
        default='default/team.jpg',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg']),
            ImageValidator((250, 250), 524288)
        ]
    )
    user = models.ForeignKey(FatUser, on_delete=models.CASCADE, related_name='teams')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Team)
def team_member_create(sender, instance, created, **kwargs):
    """Create TeamMember after creating new Team (add author of Team to TeamMember)"""
    if created:
        TeamMember.objects.create(user=instance.user, team_id=instance.pk)


class TeamMember(models.Model):
    user = models.ForeignKey(FatUser, on_delete=models.CASCADE, related_name='team_members')
    team = models.ForeignKey(Team, related_name="members", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.user} is member {self.team} team'


class Invitation(models.Model):
    """ Invitation or request to team model"""
    team = models.ForeignKey(Team, related_name="invitations", on_delete=models.CASCADE)
    user = models.ForeignKey(FatUser, on_delete=models.CASCADE, related_name='invitations')
    accepted = models.BooleanField(default=False)
    asking = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.user} - team {self.team}'


class Post(models.Model):
    """ Team`s post model"""
    text = models.TextField(max_length=1024)
    create_date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    moderation = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(FatUser, on_delete=models.CASCADE, related_name='posts')
    team = models.ForeignKey(Team, related_name="articles", on_delete=models.CASCADE)

    def __str__(self):
        return f'id {self.id}'

    def comments_count(self):
        return self.post_comments.filter(is_delete=False).count()


class Comment(models.Model):
    """ Team`s comment model """
    text = models.TextField(max_length=512)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_publish = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    user = models.ForeignKey(FatUser, on_delete=models.CASCADE, related_name='team_comments')
    post = models.ForeignKey(Post, related_name="post_comments", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return f'User {self.user} commented post {self.post}'


class SocialLink(models.Model):
    name = models.CharField(max_length=25)
    link = models.URLField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='social_links')
