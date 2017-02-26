from flask import Blueprint, request
from flask_restful import Resource, reqparse
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
        file_obj = request.files;
        file = file_obj['file']
        extension = os.path.splitext(file.filename)[1]
        id = str(uuid.uuid4())
        f_name =  id + extension
        file.save(os.path.join(os.getcwd(), 'upload/', f_name))
        file_to_save = File(id, file.filename)
        db.session.add(file_to_save)
        db.session.commit()
        return json.dumps({'filename':f_name, 'id': id})

class Coor(Resource):
    def post(self, file_id):
        args = json.loads(request.data)
        id = str(uuid.uuid4())
        if (file_id):
            fileArea = FileArea(id,
                                file_id,
                                args['top'],
                                args['left'],
                                args['bottom'],
                                args['right'])
            db.session.add(fileArea)
            db.session.commit()


class File(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    filename = db.Column(db.String(80), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, fileId, filename):
        self.id = fileId
        self.filename = filename
        # self.user_id = user_id

    def __repr__(self):
        return '<File %r>' % self.filename

class FileArea(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    file_id = db.Column(db.String(80), db.ForeignKey('file.id'))
    top = db.Column(db.Integer)
    right = db.Column(db.Integer)
    bottom = db.Column(db.Integer)
    left = db.Column(db.Integer)

    def __init__(self, id, file_id, top, right, bottom, left):
        self.id = id
        self.file_id = file_id
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left