from bson import encode
from flask import Flask, request, render_template
import pymongo
from bson.binary import Binary
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

client = pymongo.MongoClient(
    "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
)

db = client.get_database('flaskImage')
record = db.image

@app.route('/')
def index():
    return render_template('index.html')

def uploadImage(name):
    with open(name, "rb") as hoja:
        encoded = Binary(hoja.read())
    record.insert({"image" : encoded})

@app.route('/create', methods=['POST', 'GET'])
def create():
    ff = request.files['file']
    name = ff.filename
    name = name.replace(" ", "")
    ff.save(secure_filename(name))
    try:
        uploadImage(name)
        return 'Uploaded Successfully!!'
    except Exception as e:
        return 'Image Upload Failed :('

if __name__ == '__main__':
    app.run(debug=True)