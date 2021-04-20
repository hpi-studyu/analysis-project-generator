from flask import Flask, request
from flask_cors import CORS, cross_origin
from generator import generate_repo

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
@cross_origin()
def generate():
    gitlab_token = request.headers["X-Gitlab-Token"]
    supabase_token = request.headers["X-Supabase-Token"]
    study_id = request.headers["X-Study-Id"]
    generate_repo(gitlab_token,supabase_token, study_id)
    return "Finished generating repository"

if __name__ == "__main__":
    app.run()