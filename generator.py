from utils import fetchStudySchema, fill_file_templates
from gitlab_utils import create_project_file, create_project
import gitlab
from copier import run_auto
import os
import shutil
import random, string


project_path = "generated/"


def generate_repo(gitlab_token, supabase_token = None, study_id = None):

    project_title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    generate_from_template(study_title=project_title)

    gl = gitlab.Gitlab("https://gitlab.com", oauth_token=gitlab_token)

    project = create_project(gl, project_title)
    print(f'Created project: {project.name}')

    commit_actions = [
        commit_action(file_path) for file_path in walk_generated_project(project_path)
    ]

    commitData = {
        "branch": "master",
        "commit_message": "Generated project from copier-studyu\n\nhttps://github.com/hpi-studyu/copier-studyu",
        "actions": commit_actions,
    }

    commit = project.commits.create(commitData)
    print(f'Finished generating repository from template')


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
            print(os.path.relpath(os.path.join(root, name), project_path).replace(os.sep,'/'))
            yield os.path.relpath(os.path.join(root, name), project_path).replace(os.sep,'/')


def generate_from_template(study_title: str, path: str = project_path):
    print(f'Start generating project from template...')
    if os.path.isdir(path):
        shutil.rmtree(path)
    run_auto(
        src_path="gh:hpi-studyu/copier-studyu",
        dst_path=path,
        data={"study_title": study_title},
    )
    print(f'Finished generating project')
