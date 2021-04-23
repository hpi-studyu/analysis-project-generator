import json
import os
from typing import Optional

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware

from utils.generator import generate_repo
from utils.gitlab_service import GitlabService
from utils.study_data import fetch_new_study_data_with_project_id
from utils.supabase_service import SupabaseService

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def generate(
    x_session: Optional[str] = Header(None),
    x_user_id: Optional[str] = Header(None),
    x_study_id: Optional[str] = Header(None),
):
    sbs = SupabaseService(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_ANON_KEY"),
        json.loads(x_session),
    )
    gs = GitlabService(oauth_token=sbs.session["provider_token"])

    repo_id = generate_repo(sbs, gs, x_study_id)

    sbs.create_repo_entry(repo_id, x_user_id, x_study_id, "gitlab")

    return {"message": "Finished generating repository", "repo_url": repo_id}


@app.get("/repo/update")
async def update_repo(
    x_session: Optional[str] = Header(None),
    x_study_id: Optional[str] = Header(None),
    x_project_id: Optional[str] = Header(None),
):
    sbs = SupabaseService(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_ANON_KEY"),
        json.loads(x_session),
    )

    gs = GitlabService(oauth_token=sbs.session["provider_token"])

    fetch_new_study_data_with_project_id(sbs, gs, x_study_id, x_project_id, 'update')

    return {"message": "Updating repo with study data"}
