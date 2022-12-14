from .pdf2tiles import Pdf2Tiles
from app import app
import shutil
import os

PROJECT_DIR = app.config['PROJECTS_DIR']

def delete_path(project_name, page_name = None):
    project_dir = os.path.join(PROJECT_DIR, project_name)
    if page_name is not None:
        project_dir = os.path.join(project_dir, page_name)
    shutil.rmtree(project_dir)

    

