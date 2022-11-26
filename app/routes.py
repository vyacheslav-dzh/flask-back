from flask import request
from app import app
from .lib import Pdf2Tiles
from flask_cors import cross_origin
import os


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
    pdf2tiles.run(file_path)

    return '', 200


@app.route('/upload_pdf', methods=['POST', 'OPTIONS'])
def upload_pdf():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    return '', 200
