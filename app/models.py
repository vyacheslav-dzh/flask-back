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
