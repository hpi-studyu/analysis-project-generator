from typing import Dict, List

from gitlab import Gitlab
from gitlab.v4.objects import Project


class GitlabService:
    def __init__(self, oauth_token, gitlab_url="https://gitlab.com"):
        self.gl = Gitlab(gitlab_url, oauth_token=oauth_token)

    def create_user(self):
        # Create new user on own Gitlab instance
        user_data = {
            "email": "jen@foo.com",
            "username": "jen",
            "name": "Jen",
            "password": "test",
        }
        user = self.gl.users.create(user_data)
        print(user)
        return user

    def create_project(self, project_title: str) -> Project:
        return self.gl.projects.create({"name": project_title})

    def create_project_file(self, project: Project, name: str, content: dict):
        return project.files.create(
            {
                "file_path": name,
                "branch": "master",
                "content": content,
                "author_email": "test@example.com",
                "author_name": "yourname",
                "commit_message": "Create testfile",
            }
        )

    def make_commit(
        self,
        project: Project,
        message: str,
        actions: List[Dict[str, str]],
        branch: str = "master",
    ):
        commitData = {
            "branch": "master",
            "commit_message": "Generated project from copier-studyu\n\nhttps://github.com/hpi-studyu/copier-studyu",
            "actions": actions,
        }

        return project.commits.create(commitData)
