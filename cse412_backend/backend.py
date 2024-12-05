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
    _result = result.fetchall()
    keys = result.keys()
    return [dict(zip(keys, r)) for r in _result]  # fun one-liner


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
    result = db.session.execute(text(
        "SELECT locname AS name, locaddress AS address, loctype, locdatefounded AS datefounded, locnum AS id FROM location"));
    return result_to_json(result)


@app.route("/location/<locnum>", methods=['GET'])
def location(locnum):
    # TODO: join with the appropriate table(s) to get location contact info, employees, and other pertaining info specific to locations.
    result = db.session.execute(text("SELECT locname AS name FROM location WHERE locnum = :num"), {"num": locnum})
    d = result_to_dict(result)
    if len(d) != 1:
        return '', 404
    return jsonify(d[0])


@app.route("/businesscontact/<contnum>", methods=['GET'])
def bussinesscontact(contnum):
    result = db.session.execute(text("SELECT contFName AS fname, contLName AS lname, contEmail AS email, "
                                     "contWebsite AS website, contPhone AS phone FROM "
                                     "businesscontact WHERE contNum = :contNum"), {"contNum": contnum})
    d = result_to_dict(result)
    if len(d) != 1:
        return '', 404
    return jsonify(d[0])


@app.route("/employeelist/<locnum>", methods=['GET'])
def employee_list(locnum):
    result = db.session.execute(text("SELECT empfname, emplname, empemail AS email, empnum FROM Employee "
                                     "WHERE emplocnum = :locnum"),
                                {'locnum': locnum})
    d = result_to_dict(result)
    if len(d) < 1:
        return '', 404
    return jsonify(d)


@app.route("/employee/<empnum>", methods=['GET'])
def employee_data(empnum):
    result = db.session.execute(text("SELECT * FROM Employee WHERE empnum = :empnum"), {'empnum': empnum})
    d = result_to_dict(result)
    if len(d) != 1:
        return '', 404
    return jsonify(d[0])


@app.route("/schedule/<empnum>", methods=['GET'])
def schedule_data(empnum):
    result = db.session.execute(text("SELECT * FROM schedule WHERE schempnum = :empnum"), {'empnum': empnum})

    d = result_to_dict(result)
    print(d)
    if len(d) < 0:
        return '', 404
    return jsonify(d)


@app.route("/schedule/del/<schednum>", methods=['DELETE'])
def schedule_del(schednum):
    try:
        print(schednum)
        db.session.execute(text("DELETE FROM schedule WHERE schnum = :schednum"), {'schednum': schednum})
        db.session.commit()
    except Exception as e:
        print(e)
        return '', 500
    return '', 200


# DAY_NUM_TO_STR = {
#     1: 'Sunday',
#     2: 'Monday',
#     3: 'Tuesday',
#     4: 'Wednesday',
#     5: 'Thursday',
#     6: 'Friday',
#     7: 'Saturday'
# }
# get list of employees who work on a certain day
@app.route("/employee/<location>/<day>", methods=['GET'])
def workday_data(location, day):
    result = db.session.execute(text('SELECT empFName, empLName FROM '
                                     'Schedule INNER JOIN Employee ON schEmpNum = empNum '
                                     'WHERE schDay = :daystr AND emplocnum = :location;'), {'daystr': day, 'location': location})
    d = result_to_dict(result)
    if len(d) < 0:
        return '', 404
    print(d)
    return jsonify(d)


@app.route("/employee/pay/<empnum>", methods=['GET'])
def pay_data(empnum):
    result = db.session.execute(text('SELECT schEmpNum AS "Employee Number", empFName AS "Employee First Name", '
                                     'empLName AS "Employee Last Name", SUM(schPay) AS "Total Pay by Employee" '
                                     'FROM Schedule INNER JOIN Employee ON Schedule.schEmpNum = Employee.empNum '
                                     'WHERE schEmpNum  = :empnum GROUP BY schEmpNum, empFName, empLName;'),
                                {'empnum': empnum})
    d = result_to_dict(result)
    if len(d) != 1:
        return '', 404
    return jsonify(d[0])


def main():
    app.run(port=6969)
