import json
import os

from dotenv import load_dotenv

from utils.copier import generate_files_from_template
from utils.gitlab_service import GitlabService
from utils.study_data import fetch_new_study_data
from utils.supabase_service import SupabaseService

load_dotenv()


def generate_repo(sbs: SupabaseService, gs: GitlabService, study_id: str):

    study = sbs.fetch_study(study_id)

    generate_files_from_template(
        study_title=study["title"], path=os.environ.get("PROJECT_PATH")
    )

    project = gs.create_project(study["title"])
    print(f"Created project: {project.name}")

    generate_initial_commit(gs, project)
    print("Committed initial files")

    fetch_new_study_data(sbs, gs, study_id, project)
    print("Fetched newest study data")

    return project.id


def generate_initial_commit(gs, project):
    commit_actions = [
        commit_action(file_path, os.environ.get("PROJECT_PATH"))
        for file_path in walk_generated_project(os.environ.get("PROJECT_PATH"))
    ]

    return gs.make_commit(
        project=project,
        message="Generated project from copier-studyu\n\nhttps://github.com/hpi-studyu/copier-studyu",
        actions=commit_actions,
    )


def commit_action(file_path: str, project_path: str, action: str = "create"):
    return {
        "action": action,
        "file_path": file_path,
        "content": open(os.path.join(project_path, file_path)).read(),
    }


def walk_generated_project(project_path):
    for root, dirs, files in os.walk(project_path):
        for name in files:
            yield os.path.relpath(os.path.join(root, name), project_path).replace(
                os.sep, "/"
            )
