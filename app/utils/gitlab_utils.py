import gitlab


def create_user(gl):
    # Create new user on own Gitlab instance
    user_data = {
        "email": "jen@foo.com",
        "username": "jen",
        "name": "Jen",
        "password": "test",
    }
    user = gl.users.create(user_data)
    print(user)
    return user


def create_project(gl, project_title: str):
    return gl.projects.create({"name": project_title})


def create_project_file(gl, project, name: str, content: dict):
    return project.files.create(
        {
            "file_path": name,
            "branch": "master",
            "content": content,
            "author_email": "test@example.com",
            "author_name": "yourname",
            "commit_message": "Create testfile",
        }
    )
