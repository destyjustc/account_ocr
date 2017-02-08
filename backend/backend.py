#!flask/bin/python
from flask import Flask, request
import os
import json
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    p = os.path.join(os.getcwd(), 'upload')
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(os.getcwd(), 'upload/', f_name))
        return json.dumps({'filename':f_name})

if __name__ == '__main__':
    app.run(debug=True)