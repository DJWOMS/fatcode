from datetime import datetime
from typing import List

from src.team.models import TeamMember


class Category(Schema):
    id: int
    name: str


class CategoryParent(Category):
    parent: Category = None


class Toolkit(Schema):
    id: int
    name: str


class ToolkitParent(Toolkit):
    parent: Toolkit = None


class User(Schema):
    id: int
    username: str
    avatar: str = None


class TeamMemberSchema(ModelSchema):
    user: User = None

    class Config:
        model = TeamMember
        model_fields = ['id', 'user']


class Team(Schema):
    id: int
    name: str
    avatar: str = None
    members: List[TeamMemberSchema] = None


class Project(Schema):
    id: int
    name: str
    description: str
    avatar: str
    user: User
    category: Category
    toolkit: List[Toolkit]
    team: Team = None
    repository: str
    create_date: datetime
    star_count: int = None
    fork_count: int = None
    commit_count: int = None
    last_commit: datetime = None


class ProjectCreate(Schema):
    name: str
    description: str
    category_id: int
    toolkit: List[int]
    team_id: int
    repository: str


class ProjectUpdate(Schema):
    name: str
    description: str
    category_id: int
    toolkit: List[int]


class Filters(Schema):
    fork_min: int = 0
    fork_max: int = 1000
    star_min: int = 0
    star_max: int = 1000
    commit_min: int = 0
    commit_max: int = 1000
    last_commit_min: int = 1
    last_commit_max: int = 365
    category_id: int = None
    toolkit: int = None
    name: str = None
