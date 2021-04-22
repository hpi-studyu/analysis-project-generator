from typing import Optional

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware

from utils.generator import generate_repo

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
    x_study_id: Optional[str] = Header(None),
):
    generate_repo(x_session, x_study_id)
    return {"message": "Finished generating repository"}
