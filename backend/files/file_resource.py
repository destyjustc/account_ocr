from flask import Blueprint, request
from flask_restful import Resource, reqparse
import os
import uuid
import json
from user.user import db, User
from PIL import Image
from ai.OCRtest import pipeline


class Upload(Resource):
    def get(self, id):
        print(id)
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
        args = json.loads(request.data.decode('utf-8'))
        id = str(uuid.uuid4())
        if (file_id):
            file = File.query.get(file_id)
            extension = os.path.splitext(file.filename)[1]
            img = Image.open(os.path.join(os.getcwd(), 'upload/', file.id+extension))
            index = 0
            while True:
                fn = str(index)+'_'+file.id
                file_area_found = FileArea.query.filter_by(filename = fn).first()
                if file_area_found:
                    index+=1
                else:
                    break
            img2 = img.crop((args['left'], args['top'], args['right'], args['bottom']))
            # img2 = img.crop((0,0,100,100))
            img2name = os.path.join(os.getcwd(), 'upload/', fn + extension)
            img2.save(img2name)
            result1, result2 = pipeline(img2name)
            fileArea = FileArea(id,
                                file_id,
                                fn,
                                args['top'],
                                args['left'],
                                args['bottom'],
                                args['right'])
            db.session.add(fileArea)
            db.session.commit()
            return json.dumps({'filename': fn+extension, 'id': id, 'locations':result1, 'results':result2})


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
    filename = db.Column(db.String(80), unique=False)
    top = db.Column(db.Integer)
    right = db.Column(db.Integer)
    bottom = db.Column(db.Integer)
    left = db.Column(db.Integer)

    def __init__(self, id, file_id, filename, top, right, bottom, left):
        self.id = id
        self.file_id = file_id
        self.filename = filename
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left