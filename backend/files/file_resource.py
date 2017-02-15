from flask import Blueprint, request
from flask_restful import Resource
import os
import uuid
import json

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