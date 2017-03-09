#!flask/bin/python
from flask import Flask, request, Blueprint, send_from_directory
from flask_restful import Api
from flask_cors import CORS, cross_origin
# from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
import os
import json
import uuid
import json
import pprint as pp
from files.file_resource import Upload, Coor, Csv
from user.user import User, db

DEBUG = True

def read_config():
    with open('config.json') as config_file:
        data = json.load(config_file)
        return data

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
config = read_config()
if DEBUG:
    pp.pprint(config)
app.config['SQLALCHEMY_DATABASE_URI'] = config['db_url']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['APPLICATION_ROOT'] = "/api"
db.app = app
db.init_app(app)

api.add_resource(Upload, '/api/upload', '/api/upload/<string:id>')
api.add_resource(Coor, '/api/coors/<string:file_id>')
api.add_resource(Csv, '/api/csv/<string:file_id>')
app.register_blueprint(api_bp)

@app.route('/api/file/<path:path>')
def send_file(path):
    return send_from_directory('upload', path)


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