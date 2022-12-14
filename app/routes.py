# -*- coding: utf-8 -*-

from flask import request, jsonify, send_file
from app import app, db
from .lib import Pdf2Tiles
from flask_cors import cross_origin
import os

from .models import Project, Page, Layer, User, Marker, Comment


@app.route('/add_project', methods=['POST', 'OPTIONS'])
@cross_origin()
def add_project():
    response = request.json
    project_name = response['projectName']
    pages = response['pagesList']

    for page in pages:
        page['pageNum'] = int(page['pageNum'])

    filename = response['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf2tiles = Pdf2Tiles(project_name, pages)
    path_list = pdf2tiles.run(file_path)

    project = Project(
        name=project_name
    )

    db.session.add(project)
    db.session.commit()

    project_id = project.id

    for i in range(len(pages)):
        page = Page(
            project_id=project_id,
            name=pages[i]['pageName'],
            path=path_list[i]['path'],
            max_zoom=path_list[i]['zoom']
        )
        db.session.add(page)
        db.session.commit()

    return '', 200


@app.route('/upload_pdf', methods=['POST', 'OPTIONS'])
def upload_pdf():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    return '', 200


@app.route("/projects", methods=["GET"])
def get_projects():
    response = Project.query.all()
    return jsonify([i.serialize for i in response])


@app.route("/pages/<int:id>", methods=["GET"])
def get_pages(id):
    response = Page.query.filter(Page.project_id == id).all()
    return jsonify([i.serialize for i in response])


@app.route("/get_tile/<string:project_name>/<string:page_name>/<int:z>/<int:x>x<int:y>.png", methods=["GET"])
def get_tile(project_name, page_name, z, x, y):
    try:
        path = os.path.join(app.config['PROJECTS_DIR'], f'{project_name}\\{page_name}\\{z}\\{y}x{x}.png')
        return send_file(path)
    except FileNotFoundError:
        return '', 404


@app.route('/add_layer', methods=['POST', 'OPTIONS'])
@cross_origin()
def add_layer():
    response = request.json
    page_id = response['pageId']
    layer_name = response['layerName']

    layer = Layer(
        page_id=page_id,
        name=layer_name
    )
    db.session.add(layer)
    db.session.commit()

    return '', 200


@app.route('/add_marker', methods=['POST', 'OPTIONS'])
@cross_origin()
def add_marker():
    response = request.json
    layer_id = response['layerId']
    header = response['header']
    text = response['text']
    x = response['x']
    y = response['y']
    color = response['color']

    marker = Marker(
        layer_id=layer_id,
        header=header,
        text=text,
        x_axis=x,
        y_axis=y,
        color=color
    )

    db.session.add(marker)
    db.session.commit()

    return '', 200


@app.route('/add_comment', methods=['POST', 'OPTIONS'])
@cross_origin()
def add_comment():
    response = request.json
    marker_id = response['markerId']
    user_id = response['userId']
    text = response['text']
    date = response['date']

    comment = Comment(
        marker_id=marker_id,
        user_id=user_id,
        text=text,
        date=date
    )

    db.session.add(comment)
    db.session.commit()

    return '', 200


@app.route("/layers/<int:id>", methods=["GET"])
def get_layers(id):
    response = Layer.query.filter(Layer.page_id == id).all()
    return jsonify([i.serialize for i in response])


@app.route("/markers/<int:id>", methods=["GET"])
def get_markers(id):
    response = Marker.query.filter(Marker.layer_id == id).all()
    return jsonify([i.serialize for i in response])


@app.route("/comments/<int:id>", methods=["GET"])
def get_comments(id):
    response = Comment.query.filter(Comment.marker_id == id).all()
    return jsonify([i.serialize for i in response])


@app.route("/users", methods=["GET"])
def get_users():
    response = User.query.all()
    return jsonify([i.serialize for i in response])


# @app.route('/delete_table', methods=['GET'])
# def delete_tables():
#     Project.query.delete()
#     Page.query.delete()
#     db.session.commit()
#     return '', 200
