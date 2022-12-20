from .pdf2tiles import Pdf2Tiles
from app import app
import shutil
import os

PROJECT_DIR = app.config['PROJECTS_DIR']

def delete_path(project_id, page_id = None):
    project_dir = os.path.join(PROJECT_DIR, str(project_id))
    if page_id is not None:
        project_dir = os.path.join(project_dir, str(page_id))
    shutil.rmtree(project_dir)


# def rename_project_path(old_name, new_name):
#     project_dir_old = os.path.join(PROJECT_DIR, old_name)
#     project_dir_new = os.path.join(PROJECT_DIR, new_name)
#     os.rename(project_dir_old, project_dir_new)


# def rename_page_path(project_name, old_page_name, new_page_name):
#     project_dir = os.path.join(PROJECT_DIR, project_name)
#     page_dir_old = os.path.join(project_dir, old_page_name)
#     page_dir_new = os.path.join(project_dir, new_page_name)
#     os.rename(page_dir_old, page_dir_new)

