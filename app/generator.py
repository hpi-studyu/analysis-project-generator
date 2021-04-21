from utils import fetchStudySchema, fill_file_templates
from gitlab_utils import create_project_file, create_project
import gitlab
from copier import run_auto
import os
import shutil
import random, string
from supabase_py import create_client, Client
from dotenv import load_dotenv
import json

load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_anon_key = os.environ.get("SUPABASE_ANON_KEY")
project_path = os.environ.get("PROJECT_PATH")


def fetch_study(supabase_token, study_id):
    supabase: Client = create_client(supabase_url, supabase_anon_key)

    study = supabase.table("study").select("*").eq("id", study_id).single().execute()
    print(study["data"])
    return study["data"]


def generate_repo(gitlab_token, supabase_token, study_id):

    study = fetch_study(supabase_token, study_id)

    generate_from_template(study_title=study["title"])

    gl = gitlab.Gitlab("https://gitlab.com", oauth_token=gitlab_token)

    project = create_project(gl, study["title"])
    print(f"Created project: {project.name}")

    commit_actions = [
        commit_action(file_path) for file_path in walk_generated_project(project_path)
    ]
    commit_actions.append(
        {
            "action": "create",
            "file_path": "study.schema.json",
            "content": json.dumps(study, indent = 4),
        }
    )

    commitData = {
        "branch": "master",
        "commit_message": "Generated project from copier-studyu\n\nhttps://github.com/hpi-studyu/copier-studyu",
        "actions": commit_actions,
    }

    commit = project.commits.create(commitData)
    print(f"Finished generating repository from template")


def commit_action(
    file_path: str, project_path: str = project_path, action: str = "create"
):
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


def generate_from_template(study_title: str, path: str = project_path):
    print(f"Start generating project from template...")
    if os.path.isdir(path):
        shutil.rmtree(path)
    run_auto(
        src_path="gh:hpi-studyu/copier-studyu",
        dst_path=path,
        data={"study_title": study_title},
    )
    print(f"Finished generating project")
