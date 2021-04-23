import json
from typing import Dict, List

from gitlab.v4.objects import Project

from utils.gitlab_service import GitlabService
from utils.supabase_service import SupabaseService


def fetch_new_study_data_with_project_id(
    sbs: SupabaseService, gs: GitlabService, study_id: str, project_id: str
):
    project = gs.fetch_project(project_id)
    fetch_new_study_data(sbs, gs, study_id, project)


def fetch_new_study_data(
    sbs: SupabaseService, gs: GitlabService, study_id: str, project: Project
):
    study = sbs.fetch_study(study_id)
    subjects = sbs.fetch_subjects_for_study(study["id"])

    commit_actions: List[Dict[str, str]] = []
    commit_actions.append(
        {
            "action": "update",
            "file_path": "data/study.schema.json",
            "content": json.dumps(study, indent=4),
        }
    )

    commit_actions.append(
        {
            "action": "update",
            "file_path": "data/subjects.json",
            "content": json.dumps(subjects, indent=4),
        }
    )

    gs.make_commit(
        project=project,
        message="Fetch newest data from database",
        actions=commit_actions,
    )
