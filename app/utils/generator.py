import json
import os

from dotenv import load_dotenv

from utils.copier import generate_files_from_template
from utils.gitlab_service import GitlabService
from utils.supabase_service import SupabaseService

load_dotenv()


def generate_repo(session, study_id):
    supabase_session = json.loads(session)

    sbs = SupabaseService(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_ANON_KEY"),
        supabase_session,
    )
    study = sbs.fetch_study(study_id)
    subjects = sbs.fetch_subjects_for_study(study["id"])

    generate_files_from_template(
        study_title=study["title"], path=os.environ.get("PROJECT_PATH")
    )

    gs = GitlabService(oauth_token=supabase_session["provider_token"])

    project = gs.create_project(study["title"])
    print(f"Created project: {project.name}")

    generate_initial_commit(gs, project, study, subjects)

    print(f"Committed initial project")


def generate_initial_commit(gs, project, study, subjects):
    commit_actions = [
        commit_action(file_path, os.environ.get("PROJECT_PATH"))
        for file_path in walk_generated_project(os.environ.get("PROJECT_PATH"))
    ]

    commit_actions.append(
        {
            "action": "create",
            "file_path": "data/study.schema.json",
            "content": json.dumps(study, indent=4),
        }
    )

    commit_actions.append(
        {
            "action": "create",
            "file_path": "data/subjects.json",
            "content": json.dumps(subjects, indent=4),
        }
    )

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
            print(
                os.path.relpath(os.path.join(root, name), project_path).replace(
                    os.sep, "/"
                )
            )
            yield os.path.relpath(os.path.join(root, name), project_path).replace(
                os.sep, "/"
            )
