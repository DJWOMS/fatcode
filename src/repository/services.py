from github import Github
from . import utils
from .interfaces import Repository
from ..team.models import Team
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import APIException
import requests
from . import models
from ..base import exceptions

github = Github()

def get_id(user):
    """Поиск nik в github пользователя"""
    try:
        account_id = user.user_account.filter(provider='github').first().account_id
        return account_id
    except:
        raise exceptions.BadAccount()
        # raise APIException(
        #     detail='Добавить репозиторий возможно только для аккаунтов привязанных к github',
        #     code=status.HTTP_400_BAD_REQUEST
        # )

def get_my_repository(repository, account_id):
    """Поиск репозитория пользователя"""
    nik = get_nik(repository, account_id)
    user_repos = get_user_repos(nik)
    cur_repo = repository.split('/')[-1]
    if cur_repo in user_repos:
        return cur_repo, nik
    else:
        raise exceptions.BadAccountAuthor()

def get_nik(repository, account_id):
    cur_nik = repository.split('/')[-2]
    user_info = requests.get(f'https://api.github.com/users/{cur_nik}/repos').json()
    cur_id = user_info[0]['owner']['id']
    if str(cur_id) == account_id:
        return cur_nik
    else:
        # raise APIException(
        #     detail='Bad account_id',
        #     code=status.HTTP_400_BAD_REQUEST
        # )
        raise exceptions.BadAccountId()

def get_user_repos(nik):
    """Поиск всех репозиториев пользователя"""
    user_info = requests.get(f'https://api.github.com/users/{nik}/repos')
    repos = user_info.json()
    user_repos = []
    for repo in repos:
        user_repos.append(repo.get('name'))
    return user_repos

def get_stars_count(nik, repo):
    """Получение колличества звезд репозитория"""
    repo_info = requests.get('https://api.github.com/repos/' + nik + '/' + repo)
    stars = repo_info.json()['stargazers_count']
    return stars

def get_forks_count(nik, repo):
    """Получение колличества форков репозитория"""
    repo_info = requests.get('https://api.github.com/repos/' + nik + '/' + repo)
    forks_count = repo_info.json()['forks_count']
    return forks_count

def get_last_commit(nik, repo):
    """Получение даты последнего комментария репозитория"""
    repo_info = requests.get(f'https://api.github.com/repos/{nik}/{repo}/commits')
    last_commit = repo_info.json()[0]['commit']['author']['date']
    return last_commit

def get_commits_count(nik, repo):
    """Получение даты последнего комментария репозитория"""
    repo_info = requests.get(f'https://api.github.com/repos/{nik}/{repo}/commits')
    commits_count = 0
    commits = repo_info.json()
    for commit in commits:
        commits_count += 1
    return commits_count

def get_repository(repository):
    return github.get_repo(f'{"/".join(repository.split("/")[-2:])}')

def get_projects_stats(projects):
    for project in projects:
        repository = get_repository(project.repository)
        utils.repository_stats(project, repository)
    return projects

def get_project_stats(project):
    repository = get_repository(project.repository)
    utils.repository_stats(project, repository)
    return project

def get_repo(repository, account_id) -> Repository:
    repo, nik = get_my_repository(repository, account_id)
    stars_count = get_stars_count(nik, repo)
    forks_count = get_forks_count(nik, repo)
    commits_count = get_commits_count(nik, repo)
    last_commit = get_last_commit(nik, repo)
    return Repository(stars_count, forks_count, commits_count, last_commit)

def check_teams(teams):
    for team in teams:
        cur_team = models.Project.objects.filter(teams=team).exists()
        if cur_team:
            raise exceptions.TeamExists()
            # raise APIException(
            #     detail='Для данной команды есть проект',
            #     code=status.HTTP_400_BAD_REQUEST
            #     )
    return teams

def check_my_teams(teams, user):
    try:
        for team in teams:
            team = Team.objects.get(
                Q(user=user) &
                Q(id=team.id)
            )
        return True
    except Team.DoesNotExist:
        raise exceptions.TeamAuthor()
        # raise APIException(
        #     detail='Создать возможно только для своей команды',
        #     code=status.HTTP_400_BAD_REQUEST
        # )

def check_repo(repo):
    try:
        repository = models.Project.objects.get(repository=repo)
        raise exceptions.RepositoryExists()
        # raise APIException(
        #     detail='Для данного репозитория уже есть проект',
        #     code=status.HTTP_400_BAD_REQUEST
        # )
    except models.Project.DoesNotExist:
        return True

def get_info_for_user(repository, teams, user):
    if check_repo(repository) and check_teams(teams) and check_my_teams(teams, user):
        return get_id(user)

def check_instance_repo(pk, repository):
    repo = models.Project.objects.filter(id=pk, repository=repository).exists()
    return repo

def check_instance_teams(teams, pk):
    for team in teams:
        team = models.Project.objects.filter(id=pk, teams=team).exists()
        if not team:
            return False
    return teams

def get_info_for_user_update(repository, teams, user, pk):
    if check_instance_repo(pk, repository):
        return check_all_teams_to_update(teams, pk, user)
    if check_repo(repository):
        return check_all_teams_to_update(teams, pk, user)

def check_all_teams_to_update(teams, pk, user):
    if check_instance_teams(teams, pk):
        if check_my_teams(teams, user):
            cur_user = get_id(user)
            return cur_user
    else:
        if check_teams(teams) and check_my_teams(teams, user):
            return get_id(user)

def project_create(repo_info, user, repository, teams, toolkit, **validated_data):
    project = models.Project.objects.create(
        star=repo_info.stars_count,
        fork=repo_info.forks_count,
        commit=repo_info.commits_count,
        last_commit=repo_info.last_commit,
        user=user,
        repository=repository,
        **validated_data
    )
    for team in teams:
        project.teams.add(team)
    for toolkit in toolkit:
        project.toolkit.add(toolkit)
    return project

def project_update(instance, repo_info, teams, toolkits):
    instance.teams.clear()
    instance.toolkit.clear()
    for team in teams:
        instance.teams.add(team)
    for toolkit in toolkits:
        instance.toolkit.add(toolkit)
    instance.stars_count = repo_info.stars_count
    instance.forks_count = repo_info.forks_count
    instance.commits_count = repo_info.commits_count
    instance.last_commit = repo_info.last_commit
    return instance