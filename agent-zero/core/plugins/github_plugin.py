"""GitHub plugin for agent-zero."""
from typing import List
from github import Github
from git import Repo

def list_repos(token: str) -> List[str]:
    gh = Github(token)
    return [repo.full_name for repo in gh.get_user().get_repos()]

def clone_repo(url: str, dest: str) -> None:
    Repo.clone_from(url, dest)
