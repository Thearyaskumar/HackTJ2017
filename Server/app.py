from flask import Flask, request, redirect, url_for, make_response, abort, jsonify
from werkzeug import secure_filename, Response
from pymongo import MongoClient
from bson.objectid import ObjectId
from gridfs import GridFS
from gridfs.errors import NoFile
from flask_pymongo import PyMongo
import datetime
now = datetime.datetime.now()

DB = MongoClient().app
FS = GridFS(DB)
app = Flask(__name__)
mongoData = PyMongo(app)

@app.route('/users/')
def list_users():
    cursor = mongoData.db.Users.find()
    data = []
    for user in cursor:
        data.append(user.get("Name"))
    return jsonify(data)

@app.route('/users/<username>')
def list_files(username):
    cursor = mongoData.db.fs.files.find({"user":username})
    data = []
    for file in cursor:
        data.append({"url":url_for('get_file',oid=str(file.get("_id"))),"ts":file.get("ts")})
    return jsonify(data)

@app.route('/files/<oid>')
def get_file(oid):
    try:
        file = FS.get(ObjectId(oid))
        return Response(file, mimetype=file.content_type, direct_passthrough=True)
    except NoFile:
        abort(404)

@app.route('/upload', methods=['POST'])
def uploadFile():
    print(request.files)
    file = request.files['file']
    filename = secure_filename(file.filename)
    oid = FS.put(file, content_type=file.content_type, filename=filename, user=request.form['user'], ts=now.strftime("%Y%m%d"))
    return "Creation Successful!"

@app.route('/login', methods=['POST'])
def login():
    user = mongoData.db.Users.find({"Name":request.form['user']})
    return str(request.form['pass']==user.next().get('Password'))
