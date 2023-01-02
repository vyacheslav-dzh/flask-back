import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
    UPLOAD_FOLDER = os.path.join(basedir, 'downloads')
    PROJECTS_DIR = os.path.join(basedir, 'projects')
    BASE_DIR = basedir
    # UPLOAD_FOLDER = 'C:\\Работа\\Гуртяков\\flask-back\\app\\downloads'
    # PROJECTS_DIR = 'C:\\Работа\\Гуртяков\\flask-back\\projects'
