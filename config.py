import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOADED_PHOTOS_DEST = os.getcwd() + '/uploads'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://root:maitree@localhost/userr'   #created my own database
    SQLALCHEMY_TRACK_MODIFICATIONS = False