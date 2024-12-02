from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

from sqlalchemy import text

app = Flask(__name__)
app.config.from_object('cse412_backend.config.Config')

CORS(app)
db = SQLAlchemy(app)

def result_to_dict(result):
    results = result.fetchall()
    keys = list(result.keys())
    # let me know if there's a better way to do this...
    ret = []
    for result in results:
        thing = {}
        for i, part in enumerate(result):
            thing[keys[i]] = result[i]
        ret.append(thing)
    return ret
def result_to_json(result):
    return jsonify(result_to_dict(result))

@app.route("/", methods=['GET'])
def index():
    return "This is an API, you shouldn't be here...", 400

@app.route("/test", methods=['GET'])
def foo():
    result = db.session.execute(text("SELECT * FROM businesscontact"))
    return result_to_json(result)

@app.route("/locations", methods=['GET'])
def locations():
    result = db.session.execute(text("SELECT locname AS name, locaddress AS address, loctype, locdatefounded AS datefounded, locnum AS id FROM location"));
    return result_to_json(result)

@app.route("/location/<locnum>", methods=['GET'])
def location(locnum):
    # TODO: join with the appropriate table(s) to get location contact info, employees, and other pertaining info specific to locations.
    result = db.session.execute(text("SELECT locname AS name FROM location WHERE locnum = :num"), {"num": locnum})
    d = result_to_dict(result)
    if len(d) != 1:
        return '', 404
    return jsonify(d[0])

def main():
    app.run(port=6969)
