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
    a = result.fetchall()
    b = result.keys()
    return str(b) + "\n\n" + '\n'.join(str(a).split('), '))


def main():
    app.run(port=6969)
