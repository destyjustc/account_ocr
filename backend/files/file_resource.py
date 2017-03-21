from flask import Blueprint, request
from flask_restful import Resource, reqparse
import os
import uuid
import json
from user.user import db, User
from PIL import Image
from ai.OCRtest import pipeline, findLineLocations
from sqlalchemy.dialects.postgresql import JSON
import csv
import math
from wand.image import Image as im
from itertools import zip_longest

MIN_ROW_HEIGHT = 30

class Upload(Resource):
    def get(self, id):
        print(id)
        return json.dumps({"error": "file not found"})
    def post(self):
        p = os.path.join(os.getcwd(), 'upload')
        file_obj = request.files;
        file = file_obj['file']
        file_name_pre = os.path.splitext(file.filename)[0]
        extension = os.path.splitext(file.filename)[1]
        file_id = str(uuid.uuid4())
        f_name = file_id + extension
        if file.content_type and file.content_type == 'application/pdf':
            path = os.path.join(os.getcwd(), 'upload/', f_name)
            file.save(path)
            img = im(filename=path, resolution=300)
            img.compression_quality = 99
            lst = []
            for i in range(0, len(img.sequence)):
                id = str(uuid.uuid4())
                path = os.path.join(os.getcwd(), 'upload/', id+'.png')
                temp = im(img.sequence[i])
                temp.alpha_channel = False
                temp.save(filename=path)
                file_to_save = File(id, file_name_pre + '-' + str(i) +'.png')
                db.session.add(file_to_save)
                db.session.commit()
                lst.append({'filename':id +'.png', 'id': id})
            return json.dumps(lst)
        elif file.content_type and file.content_type.split('/')[0]=='image':
            file.save(os.path.join(os.getcwd(), 'upload/', f_name))
            file_to_save = File(file_id, file.filename)
            db.session.add(file_to_save)
            db.session.commit()
            return json.dumps([{'filename':f_name, 'id': file_id}])

class Csv(Resource):
    def get(self, file_id):
        areas = FileArea.query.filter_by(file_id=file_id).order_by(FileArea.filename).all()
        ret = []
        for i in areas:
            print(i)
            if i.corrected:
                ret.append(json.loads(i.corrected))
            else:
                ret.append(json.loads(i.result))
        print(type(ret[0][0]))
        print(ret[0])
        if len(ret):
            fn = areas[0].file_id+'.csv'
            path = os.path.join(os.getcwd(), 'upload/', fn)
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f, dialect='excel')
                writer.writerows(zip_longest(*ret))
        return json.dumps(fn)

class Coor(Resource):
    def post(self, file_id):
        args = json.loads(request.data.decode('utf-8'))
        id = str(uuid.uuid4())
        if (file_id):
            file = File.query.get(file_id)
            radio = file.radio
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
            # result1, result2 = pipeline(img2name)
            result1 = findLineLocations(img2name)
            if radio == 0 and result1 and len(result1):
                radio = math.floor(MIN_ROW_HEIGHT/(result1[0][1]-result1[0][0]))
                file.radio = radio
                db.session.commit()
            if radio > 1:
                img3 = img2.resize((img2.width*radio, img2.height*radio) , Image.ANTIALIAS)
                # img3name = os.path.join(os.getcwd(), 'upload/', fn + '_resized' + extension)
                img3.save(img2name)
            result1, result2, prob = pipeline(img2name)
            # lst = getResizedLocations(result1, radio)
            fileArea = FileArea(id,
                                file_id,
                                fn,
                                args['top'],
                                args['left'],
                                args['bottom'],
                                args['right'],
                                json.dumps(result2),
                                json.dumps(result2))
            db.session.add(fileArea)
            db.session.commit()
            return json.dumps({'filename': fn + extension, 'id': id, 'locations':result1, 'results':result2})
    def put(self, file_id):
        args = json.loads(request.data.decode('utf-8'))
        print(request)
        for i in args:
            record = FileArea.query.filter_by(id=i['id']).first()
            record.corrected = json.dumps(i['results'])
            db.session.commit()
            print('hello')




class File(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    filename = db.Column(db.String(80), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    radio = db.Column(db.Integer)

    def __init__(self, fileId, filename):
        self.id = fileId
        self.filename = filename
        self.radio = 0
        # self.user_id = user_id

    def __repr__(self):
        return '<File %r>' % self.filename

class FileAreaResource(Resource):
    def put(self):
        print(request)

class FileArea(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    file_id = db.Column(db.String(80), db.ForeignKey('file.id'))
    filename = db.Column(db.String(80), unique=False)
    top = db.Column(db.Integer)
    right = db.Column(db.Integer)
    bottom = db.Column(db.Integer)
    left = db.Column(db.Integer)
    result = db.Column(JSON)
    corrected = db.Column(JSON)

    def __init__(self, id, file_id, filename, top, right, bottom, left, result, corrected):
        self.id = id
        self.file_id = file_id
        self.filename = filename
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
        self.result = result
        self.corrected = corrected