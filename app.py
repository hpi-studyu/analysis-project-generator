from flask import Flask, request
from flask_cors import CORS, cross_origin
from generator import generate_repo

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
@cross_origin()
def generate():
    token = request.headers["X-Gitlab-Token"]
    generate_repo(gitlab_token=token)
    return "Finished generating repository"

if __name__ == "__main__":
    app.run()