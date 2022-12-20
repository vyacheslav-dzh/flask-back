# -*- coding: utf-8 -*-

from flask import request, jsonify, send_file
from app import app, db
from .lib import Pdf2Tiles, delete_path, rename_project_path, rename_page_path
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


    project = Project(
        name=project_name
    )

    db.session.add(project)
    db.session.commit()

    project_id = project.id

    pages_id_list = []
    for i in range(len(pages)):
        page = Page(
            project_id=project_id,
            name=pages[i]['pageName'],
            path="null",
            max_zoom=0
        )
        db.session.add(page)
        db.session.commit()
        pages_id_list.append(page.id)
    
    filename = response['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf2tiles = Pdf2Tiles(project_name, pages, project_id, pages_id_list)
    path_list = pdf2tiles.run(file_path)

    
    for i in range(len(pages_id_list)):
        page = Page.query.get(pages_id_list[i])
        page.max_zoom = path_list[i]["zoom"]
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


@app.route('/add_layer', methods=['POST'])
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


@app.route('/add_marker', methods=['POST'])
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


@app.route('/add_comment', methods=['POST'])
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


@app.route("/user/<int:id>", methods=["GET"])
def get_user(id):
    response = User.query.get(id)
    return jsonify(response.serialize)


@app.route("/delete_user/<int:id>", methods=["GET"])
def delete_user(id):
    user = User.query.get(id)

    comments = Comment.query.filter(Comment.user_id == id).all()
    for comment in comments:
        db.session.delete(comment)

    db.session.delete(user)
    db.session.commit()
    return '', 200


@app.route("/delete_project/<int:id>", methods=["GET"])
def delete_project(id):
    project = Project.query.get(id)
 
    # for page in Page.query.filter(Page.project_id == id).all():
    #     for layer in Layer.query.filter(Layer.page_id == page.id).all():
    #         for marker in Marker.query.filter(Marker.layer_id == layer.id).all(): 
    #             for comment in Comment.query.filter(Comment.marker_id == marker.id).all():
    #                 db.session.delete(comment)
    #             db.session.delete(marker)
    #         db.session.delete(layer)
    #     db.session.delete(page)

    db.session.delete(project)
    db.session.commit()

    delete_path(project.id)

    return '', 200


@app.route("/delete_page/<int:id>", methods=["GET"])
def delete_page(id):
    page = Page.query.get(id)

    # for layer in Layer.query.filter(Layer.page_id == page.id).all():
    #     for marker in Marker.query.filter(Marker.layer_id == layer.id).all():
    #         for comment in Comment.query.filter(Comment.marker_id == marker.id).all():
    #             db.session.delete(comment)
    #         db.session.delete(marker)
    #     db.session.delete(layer)

    db.session.delete(page)
    db.session.commit()

    project = Project.query.filter(Project.id == page.project_id).one()
    delete_path(project.id, page.id)
    
    return '', 200


@app.route("/delete_layer/<int:id>", methods=["GET"])
def delete_layer(id):
    layer = Layer.query.get(id)

    # for marker in Marker.query.filter(Marker.layer_id == layer.id).all():
    #     for comment in Comment.query.filter(Comment.marker_id == marker.id).all():
    #         db.session.delete(comment)
    #     db.session.delete(marker)

    db.session.delete(layer)
    db.session.commit()
    return '', 200


@app.route("/delete_marker/<int:id>", methods=["GET"])
def delete_marker(id):
    marker = Marker.query.get(id)

    # for comment in Comment.query.filter(Comment.marker_id == marker.id).all():
    #     db.session.delete(comment)

    db.session.delete(marker)
    db.session.commit()
    return '', 200


@app.route("/delete_comment/<int:id>", methods=["GET"])
def delete_comment(id):
    comment = Marker.query.get(id)

    db.session.delete(comment)
    db.session.commit()
    return '', 200


@app.route("/update_project", methods=['POST', 'OPTIONS'])
@cross_origin()
def update_project():

    response = request.json
    project = Project.query.get(response["projectID"])

    project_old_name = project.name

    project.name = response["projectName"]
    db.session.add(project)
    db.session.commit()

    # if (project_old_name != response["projectName"]):
    #     rename_project_path(project_old_name, response["projectName"])
    
    return '', 200


@app.route("/update_page", methods=['POST', 'OPTIONS'])
@cross_origin()
def update_page():
    response = request.json
    page = Page.query.get(response["pageID"])

    page_old_name = page.name

    page.name = response["pageName"]

    db.session.add(page)
    db.session.commit()

    project = Project.query.filter(Project.id == page.project_id).one()

    # if (page_old_name != response["pageName"]):
    #    rename_page_path(project.name, page_old_name, response["pageName"])

    return '', 200


@app.route("/update_layer", methods=['POST', 'OPTIONS'])
@cross_origin()
def update_layer():
    response = request.json
    layer = Layer.query.get(response["layerID"])
    layer.name = response["layerName"]
    db.session.add(layer)
    db.session.commit()
    return '', 200


@app.route("/update_marker", methods=['POST', 'OPTIONS'])
@cross_origin()
def update_marker():
    response = request.json
    marker = Marker.query.get(response["markerID"])
    marker.header = response["markerHeader"]
    marker.text = response["markerText"]
    db.session.add(marker)
    db.session.commit()
    return '', 200


@app.route("/update_comment", methods=['POST', 'OPTIONS'])
@cross_origin()
def update_comment():
    response = request.json
    comment = Comment.query.get(response["commentID"])
    comment.text = response['commentText']
    db.session.add(comment)
    db.session.commit()
    return '', 200


# @app.route('/delete_table', methods=['GET'])
# def delete_tables():
#     Project.query.delete()
#     Page.query.delete()
#     db.session.commit()
#     return '', 200
