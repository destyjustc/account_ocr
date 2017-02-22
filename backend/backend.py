#!flask/bin/python
from flask import Flask, request, Blueprint
from flask_restful import Api
# from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
import os
import json
import uuid
import json
import pprint as pp
from files.file_resource import Upload
from user.user import User, db

DEBUG = True

def read_config():
    with open('config.json') as config_file:
        data = json.load(config_file)
        return data

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
config = read_config()
if DEBUG:
    pp.pprint(config)
app.config['SQLALCHEMY_DATABASE_URI'] = config['db_url']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.app = app
db.init_app(app)

api.add_resource(Upload, '/upload', '/upload/<string:id>')
app.register_blueprint(api_bp)


# def connect_db(config):
#     mysql = MySQL()
#     app.config['MYSQL_DATABASE_USER'] = config['database']['username']
#     app.config['MYSQL_DATABASE_PASSWORD'] = config['database']['password']
#     app.config['MYSQL_DATABASE_DB'] = config['database']['db_name']
#     app.config['MYSQL_DATABASE_HOST'] = config['database']['host']
#     mysql.init_app(app)
#     return mysql.connect()

if __name__ == '__main__':
    admin = User('admin', 'kjoshy12@gmail.com', 'admin@123')
    db.create_all()
    admin_found = User.query.filter_by(username='admin').first()
    if admin_found is None:
        db.session.add(admin)
        db.session.commit()
    pp.pprint(admin_found)
    app.run(debug=True)