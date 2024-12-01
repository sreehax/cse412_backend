from flask import Flask, jsonify, request
import json, psycopg

app = Flask(__name__)
#conn = psycopg.connect("dbname=test user=postgres")

@app.route("/", methods=['GET'])
def index():
    return "This is an API, you shouldn't be here...", 400

def main():
    app.run(port=6969)
