from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route("/users")
def users():
    data = []
    cursor = mongo.db.app.find()
    for user in cursor:
	data.append(user.get("Name"))
    return jsonify(data)

if __name__ == "__main__":
    app.run()
