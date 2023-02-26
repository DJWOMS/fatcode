from src.team import services as services_team
from src.repository import services as services_rep
from src.profiles.services import check_account, check_socials
from .models import Questionnaire


def questionnaire_create(user, teams, projects, accounts, toolkits, languages, socials, **validated_data):
    """Создание анкеты пользователя"""
    questionnaire = Questionnaire.objects.create(user=user,**validated_data)
    for team in teams:
        questionnaire.teams.add(team)
    for toolkit in toolkits:
        questionnaire.toolkits.add(toolkit)
    for project in projects:
        questionnaire.projects.add(project)
    for account in accounts:
        questionnaire.accounts.add(account)
    for language in languages:
        questionnaire.languages.add(language)
    for social in socials:
        questionnaire.socials.add(social)
    return questionnaire


def check_profile(user, teams, projects, accounts, socials):
    """Проверка пользователя для создания анкеты"""
    check_teams_and_projects = services_team.check_teams(teams, user) and services_rep.check_projects(projects, user)
    check_accounts_and_socials = check_account(accounts, user) and check_socials(user, socials)
    if check_teams_and_projects and check_accounts_and_socials:
        return user


def questionnaire_update_teams(instance, teams):
    """Обновление команд в анкете пользователя"""
    instance.teams.clear()
    for team in teams:
        instance.teams.add(team)
    return instance


def questionnaire_update_projects(instance, projects):
    """Обновление проектов в анкете пользователя"""
    instance.projects.clear()
    for project in projects:
        instance.projects.add(project)
    return instance


def questionnaire_update_accounts(instance, accounts):
    """Обновление аккаунтов в анкете пользователя"""
    instance.accounts.clear()
    for account in accounts:
        instance.accounts.add(account)
    return instance


def questionnaire_update(instance, toolkits, languages, socials):
    """Обновление анкеты пользователя"""
    instance.toolkits.clear()
    instance.languages.clear()
    instance.socials.clear()
    for toolkit in toolkits:
        instance.toolkits.add(toolkit)
    for language in languages:
        instance.languages.add(language)
    for social in socials:
        instance.socials.add(social)
    return instance