from flask import Blueprint, request
from flask_restful import Resource
import os
import uuid
import json
from user.user import db, User

class Upload(Resource):
    def get(self, id):
        print id
        return json.dumps({"error": "file not found"})
    def post(self):
        p = os.path.join(os.getcwd(), 'upload')
        if request.method == 'POST':
            file = request.files['file']
            extension = os.path.splitext(file.filename)[1]
            f_name = str(uuid.uuid4()) + extension
            file.save(os.path.join(os.getcwd(), 'upload/', f_name))
            return json.dumps({'filename':f_name})

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, filename, user_id):
        self.filename = filename
        self.user_id = user_id

    def __repr__(self):
        return '<File %r>' % self.filename