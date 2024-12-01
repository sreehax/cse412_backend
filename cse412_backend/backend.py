from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

from sqlalchemy import text

app = Flask(__name__)
app.config.from_object('cse412_backend.config.Config')

db = SQLAlchemy(app)

@app.route("/", methods=['GET'])
def index():
    return "This is an API, you shouldn't be here...", 400

@app.route("/test", methods=['GET'])
def foo():
    result = db.session.execute(text("SELECT * FROM businesscontact"))
    results = result.fetchall()
    keys = list(result.keys())
    ret = []
    for result in results:
        thing = {}
        for i, part in enumerate(result):
            thing[keys[i]] = result[i]
        ret.append(thing)
    return jsonify(ret)


def main():
    app.run(port=6969)
