from datetime import datetime
from app import db
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# engine = create_engine(db, convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))


class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), unique=True)
    #pages = db.relationship('Page', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Project {}>'.format(self.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Page(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    name = db.Column(db.Unicode(255))
    path = db.Column(db.Unicode(255))
    max_zoom = db.Column(db.Integer, default=6)

    def __repr__(self):
        return '<Page {}>'.format(self.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'path': self.path,
            'max_zoom': self.max_zoom
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Unicode(255))

    def __repr__(self):
        return '<User {}>'.format(self.login)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'login': self.login
        }


class Layer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    name = db.Column(db.Unicode(255))

    def __repr__(self):
        return '<Layer {}>'.format(self.name)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'page_id': self.page_id,
            "name": self.name
        }


class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    layer_id = db.Column(db.Integer, db.ForeignKey('layer.id'))
    header = db.Column(db.Unicode(255))
    text = db.Column(db.Unicode(255))
    x_axis = db.Column(db.Integer)
    y_axis = db.Column(db.Integer)
    color = db.Column(db.Unicode(255))

    def __repr__(self):
        return '<Layer {}>'.format(self.name)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'layer_id': self.layer_id,
            "header": self.header,
            "text": self.text,
            "coordinates": {self.x_axis, self.y_axis},
            "color": self.color
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marker_id = db.Column(db.Integer, db.ForeignKey('marker.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.Unicode(255))
    date = db.Column(db.Unicode(255))

    def __repr__(self):
        return '<Layer {}>'.format(self.name)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'marker_id': self.marker_id,
            "user_id": self.user_id,
            "text": self.text,
            "date": self.date
        }
