import os

basedir = os.path.abspath(os.path.dirname(__file__)) # relpath

class Config(object):
    MAX_LENGTH = 34
    UPLOAD_FOLDER = 'tmp/'
    # app.config['DISPLAY_FOLDER'] = 'app/static/'
    # app.config['FINAL_FOLDER'] = 'static/'
    SECRET_KEY = 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False