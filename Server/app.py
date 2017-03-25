from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route("/users")
def users():
	return "doStuff"

if __name__ == "__main__":
    app.run()
