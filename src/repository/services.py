import requests

from github import Github

from . import utils
from .interfaces import Repository
from ..team.models import Team
from . import models
from ..base import exceptions

from src.team import services as services_team


github = Github()


def get_github_account_id(user):
    """Поиск nik в github пользователя"""
    if current_user := user.user_account.filter(provider='github').first():
        return current_user.account_id
    else:
        raise exceptions.BadAccount()


def get_my_repository(repository, account_id):
    """Поиск репозитория пользователя"""
    nik = get_nik(repository, account_id)
    user_repos = get_user_repos(nik)
    current_repo = repository.split('/')[-1]
    if current_repo in user_repos:
        return current_repo, nik
    else:
        raise exceptions.BadAccountAuthor()


def get_nik(repository, account_id):
    """Поиск id github пользователя"""
    current_nik = repository.split('/')[-2]
    user_info = requests.get(f'https://api.github.com/users/{current_nik}/repos').json()
    current_id = user_info[0]['owner']['id']
    if str(current_id) == account_id:
        return current_nik
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
    return repo_info.json()['stargazers_count']


def get_forks_count(nik, repo):
    """Получение колличества форков репозитория"""
    repo_info = requests.get('https://api.github.com/repos/' + nik + '/' + repo)
    return repo_info.json()['forks_count']


def get_last_commit(nik, repo):
    """Получение даты последнего комментария репозитория"""
    repo_info = requests.get(f'https://api.github.com/repos/{nik}/{repo}/commits')
    return repo_info.json()[0]['commit']['author']['date']


def get_commits_count(nik, repo):
    """Получение даты последнего комментария репозитория"""
    repo_info = requests.get(f'https://api.github.com/repos/{nik}/{repo}/commits')
    commits_count = 0
    commits = repo_info.json()
    for commit in commits:
        commits_count += 1
    return commits_count


def get_repository(repository):
    """Получение провайдера github"""
    return github.get_repo(f'{"/".join(repository.split("/")[-2:])}')


def get_projects_stats(projects):
    """Получение звезд проектов"""
    for project in projects:
        repository = get_repository(project.repository)
        utils.repository_stats(project, repository)
    return projects


def get_project_stats(project):
    """Получение звезд проекта"""
    repository = get_repository(project.repository)
    utils.repository_stats(project, repository)
    return project


def get_repo(repository, account_id) -> Repository:
    """Получение звезд, форков, комментариев, последнего комментария проекта"""
    repo, nik = get_my_repository(repository, account_id)
    stars_count = get_stars_count(nik, repo)
    forks_count = get_forks_count(nik, repo)
    commits_count = get_commits_count(nik, repo)
    last_commit = get_last_commit(nik, repo)
    return Repository(stars_count, forks_count, commits_count, last_commit)


def check_teams(teams):
    """Проверка, есть ли у комманды уже проект"""
    for team in teams:
        current_team = models.Project.objects.filter(teams=team).exists()
        if current_team:
            raise exceptions.TeamExists()
    return teams

#
# def check_my_teams(teams, user):
#     """Проверка автора команд"""
#     for team in teams:
#         team = Team.objects.filter(user=user, id=team.id).exists()
#         if not team:
#             raise exceptions.TeamAuthor()
#     return teams


def check_repo(repo):
    """Проверка, есть ли у репозитория github уже проект"""
    project = models.Project.objects.filter(repository=repo).exists()
    if project:
        raise exceptions.RepositoryExists()
    return True


def get_info_for_user(repository, teams, user):
    """Проверка входящей информации от пользователя для создания проекта"""
    check_repo_and_teams = check_repo(repository) and check_teams(teams)
    if check_repo_and_teams and services_team.check_my_teams(teams, user):
        return get_github_account_id(user)


def check_instance_repo(pk, repository):
    """Проверка проекта для обновления"""
    return models.Project.objects.filter(id=pk, repository=repository).exists()


def check_instance_teams(teams, pk):
    """Проверка команды для обновления"""
    for team in teams:
        team = models.Project.objects.filter(id=pk, teams=team).exists()
        if not team:
            return False
    return teams


def get_info_for_user_update(repository, teams, user, pk):
    """Проверка входящей информации от пользователя для обновления проекта"""
    if check_instance_repo(pk, repository):
        return check_all_teams_to_update(teams, pk, user)
    if check_repo(repository):
        return check_all_teams_to_update(teams, pk, user)


def check_all_teams_to_update(teams, pk, user):
    """Проверка всех команд пользователя для обновления проекта"""
    if check_instance_teams(teams, pk):
        if services_team.check_my_teams(teams, user):
            return get_github_account_id(user)
    elif check_teams(teams) and services_team.check_my_teams(teams, user):
        return get_github_account_id(user)


def project_create(repo_info, user, repository, teams, toolkit, **validated_data):
    """Создание проекта"""
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
    """Обновление проекта"""
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


def check_projects(projects, user):
    """Проверка проектов пользователя"""
    if projects is not None:
        for project in projects:
            cur_project = models.ProjectMember.objects.filter(user=user, project=project).exists()
            if not cur_project:
                raise exceptions.ProjectMemberExists()
    return projects