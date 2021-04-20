import os, requests
from string import Template

APPLICATION_ID = "G2FvmuPXQnqQUPI1ZKOWsuAdoQ5jLiiEGwjdQIu6"
REST_API_KEY = "3fsPBgXqeKAqHGQx4JFAliIA4EnQ5zMdspY7hAmH"


def fill_file_templates(template_variables: dict, templates_dir: str = "templates"):
    with os.scandir(templates_dir) as templates:
        for entry in templates:
            if entry.is_file:
                path = os.path.join(templates_dir, entry.name)
                with open(path, "r") as f:
                    src = Template(f.read())
                    result = src.substitute(template_variables)
                    yield entry.name, result


def fetchStudySchema(
    object_id: str, base_url: str = "https://parseapi.back4app.com/parse"
):
    headers = {
        "X-Parse-Application-Id": APPLICATION_ID,
        "X-Parse-REST-API-Key": REST_API_KEY,
    }
    response = requests.get(
        f"{base_url}/classes/Study/{object_id}",
        headers=headers,
    )
    study_schema = response.json()
    print(study_schema["title"])
    return study_schema