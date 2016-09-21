import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ['FLASK_SECRET_KEY']
#PORT = 5000

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

S3_LOCATION = os.environ['S3_LOCATION']
S3_KEY = os.environ['S3_KEY']
S3_SECRET = os.environ['S3_SECRET']
S3_UPLOAD_DIRECTORY = os.environ['S3_DIRECTORY']
S3_BUCKET = os.environ['S3_BUCKET']



