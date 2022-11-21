import datetime
from typing import NamedTuple


class Repository(NamedTuple):
    stars_count: int
    forks_count: int
    commits_count: int
    last_commit: str
