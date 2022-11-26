from flask import request
from app import app
from .lib import Pdf2Tiles
from flask_cors import cross_origin
import os

from models import Project, Page, db_session


@app.route('/add_project', methods=['POST', 'OPTIONS'])
@cross_origin()
def add_project():
    response = request.json
    project_name = response['projectName']
    layers = response['layersList']

    for layer in layers:
        layer['layerNum'] = int(layer['layerNum'])

    filename = response['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf2tiles = Pdf2Tiles(project_name, layers)
    path_list = pdf2tiles.run(file_path)

    project = Project(
        name   = project_name
    )
    db_session.add(project)
    db_session.commit()

    project_id = project.id

    for i in range(len(layers)):
        page = Page(
            project_id = project_id,
            name   = layers[i]['layerName'],
            path = path_list[i]['path'],
            max_zoom = path_list[i]['zoom']
        )
        db_session.add(page)
        db_session.commit()

    return '', 200


@app.route('/upload_pdf', methods=['POST', 'OPTIONS'])
def upload_pdf():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    return '', 200


@app.route("/projects/", methods=["POST"])
def get_projects():
    return Project.query.all()

@app.route("/pages/<int:id>", methods=["POST"])
def get_pages(id):
    return Page.query.filter(Page.project_id==id).all()