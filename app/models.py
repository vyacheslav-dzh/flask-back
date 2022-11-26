from datetime import datetime
from app import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    pages = db.relationship('Page', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Project {}>'.format(self.name)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    name = db.Column(db.String(64))
    path = db.Column(db.String(120))
    max_zoom = db.Column(db.Integer, default=6)

    def __repr__(self):
        return '<Page {}>'.format(self.name)