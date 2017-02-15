#!flask/bin/python
from flask import Flask, request, Blueprint
from flask_restful import Api
from flaskext.mysql import MySQL
import os
import json
import uuid
import json
import pprint as pp
from files.file_resource import Upload

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
conn = {}

api.add_resource(Upload, '/upload', '/upload/<string:id>')
app.register_blueprint(api_bp)

def read_config():
    with open('config.json') as config_file:
        data = json.load(config_file)
        return data

def connect_db(config):
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = config['database']['username']
    app.config['MYSQL_DATABASE_PASSWORD'] = config['database']['password']
    app.config['MYSQL_DATABASE_DB'] = config['database']['db_name']
    app.config['MYSQL_DATABASE_HOST'] = config['database']['host']
    mysql.init_app(app)
    return mysql.connect()

if __name__ == '__main__':
    config = read_config()
    pp.pprint(config)
    conn = connect_db(config)
    print(conn)
    app.run(debug=True)