from github import Github
from . import utils
import requests

github = Github()


def get_my_repository(repository, user):
    """Поиск репозитория пользователя"""
    username = user.user_account.nickname_git
    user_repos = get_user_repos(username)
    cur_repo = repository.split('/')[-1]
    if cur_repo in user_repos:
        return True


def get_user_repos(username):
    """Поиск всех репозиториев пользователя"""
    user_info = requests.get(f'https://api.github.com/users/{username}/repos')
    repos = user_info.json()
    user_repos = []
    for repo in repos:
        r = repo.get('name')
        user_repos.append(r)
    return user_repos


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
