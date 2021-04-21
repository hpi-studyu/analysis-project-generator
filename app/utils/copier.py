import os
import shutil

from copier import run_auto


def generate_files_from_template(study_title: str, path: str):
    print(f"Start generating project from template...")
    if os.path.isdir(path):
        shutil.rmtree(path)
    run_auto(
        src_path="gh:hpi-studyu/copier-studyu",
        dst_path=path,
        data={"study_title": study_title},
    )
    print(f"Finished generating project files")
