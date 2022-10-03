from github import Github
from . import utils


github = Github()


def get_my_repository(repository, user):
    github_account = user.accounts.get(provider='GitHub')
    if github_account.account_url == repository[:repository.rfind('/')]:
        return github.get_repo(
            f"{github_account.account_name}/{repository.split('/')[-1]}"
        )


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

#
# def save_avatar(file_name: str, file: UploadFile):
#     with open(file_name, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
