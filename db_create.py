#!venv/bin/python
from migrate.versioning import api
from app import app, db

import os.path
db.create_all()
if not os.path.exists(app.config['SQLALCHEMY_MIGRATE_REPO']):
    api.create(app.config['SQLALCHEMY_MIGRATE_REPO'], 'database repository')
    api.version_control(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'])
else:
    api.version_control(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'], api.version(app.config['SQLALCHEMY_MIGRATE_REPO']))