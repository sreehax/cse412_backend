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

@app.route("/suppliers", methods=['GET'])
def suppliers():
    result = db.session.execute(text(
        "SELECT supname AS name, supaddress AS address, supcountry AS country, supnum AS id FROM supplier"));
    return result_to_json(result)

@app.route("/location/<locnum>", methods=['GET'])
def location(locnum):
    # TODO: join with the appropriate table(s) to get location contact info, employees, and other pertaining info specific to locations.
    result = db.session.execute(text("SELECT locname AS name, locnum AS num FROM location WHERE locnum = :num"), {"num": locnum})
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

@app.route("/businesscontact/suppliers", methods=['GET'])
def businesscontact_supplierlist():
    result = db.session.execute(text("SELECT consupnum as supnum, contFName AS fname, contLName AS lname, contEmail AS email, "
                                         "contWebsite AS website, contPhone AS phone FROM "
                                     "businesscontact, supplierconnects WHERE concontnum = contnum"))
    d = result_to_dict(result)
    if len(d) < 1:
        return '', 200
    return jsonify(d)


@app.route("/employeelist/<locnum>", methods=['GET'])
def employee_list(locnum):
    result = db.session.execute(text("SELECT empfname, emplname, empemail AS email, empnum FROM Employee "
                                     "WHERE emplocnum = :locnum"),
                                {'locnum': locnum})
    d = result_to_dict(result)
    if len(d) < 1:
        return '{}', 200
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
    isone = 69
    # the effect of this is that if "all" is selected, we get employees working on all days, along with the information on which day they are working
    if day == "all":
        isone = 1
    result = db.session.execute(text('SELECT empFName, empLName, schDay FROM '
                                     'Schedule INNER JOIN Employee ON schEmpNum = empNum '
                                     'WHERE (schDay = :daystr OR 1 = :isone) AND emplocnum = :location;'), {'daystr': day, 'location': location, 'isone': isone})
    d = result_to_dict(result)
    if len(d) < 0:
        return '', 404
    print(d)
    return jsonify(d)


@app.route("/employee/pay/", methods=['GET'])
def pay_data():
    result = db.session.execute(text('SELECT empFName, '
                                     'empLName, SUM(schPay) AS "totalPay" '
                                     'FROM Schedule INNER JOIN Employee ON Schedule.schEmpNum = Employee.empNum '
                                     'GROUP BY schEmpNum, empFName, empLName;'),
                                )
    d = result_to_dict(result)
    print(d)
    if len(d) < 1:
        return '', 404
    return jsonify(d)

@app.route("/ingredient/<locnum>", methods=['GET'])
def get_ingredient(locnum):
    result = db.session.execute(text('SELECT * FROM Ingredient WHERE locnum = :locnum'), {'locnum': locnum})
    d = result_to_dict(result)
    print(d)
    if len(d) < 1:
        return '', 404
    return jsonify(d)

# add an order

NUM_TO_ING = dict(zip(list(range(1,11)), ['Carrot', 'Basmati Rice', 'Green Peas', 'Garlic',
                              'Onion', 'Eggs', 'Corn Cob', 'Salt Container', 'Soy Sauce Bottle', 'Parsley']))
NUM_TO_TYPE = dict(zip(list(range(1,11)), ['Pounds', 'Pounds', 'Pounds', 'Pounds', 'Pounds', 'Dozens', 'Pounds',
                                           'Count', 'Count', 'Pounds']))

@app.route("/order/<locnum>", methods=['POST'])
def add_order(locnum):
    # i did not want to make ordnum serial so i just get the maxval of it and increment it!
    # print(db.session.execute(text("SELECT MAX(ordnum) FROM orders;")).fetchall()[0][0])
    try:
        max_val = int(db.session.execute(text("SELECT MAX(ordnum) FROM orders;")).fetchall()[0][0])
        r = request.get_json()
        print(r)
        ingredients = r.get('ingredients')
        ingredients_list = ingredients.split(',') if ',' in ingredients else [ingredients]
        supnum = r.get('supnum')
        result = db.session.execute(text("INSERT INTO orders (ordtotal, orddelivered, ordtime, "
                                    "orddate, ordingnumlist, ordsupnum, ordlocnum, ordnum) VALUES "
                                    "(10, '3', '12:00', '12/06/24', :ingredients, :supnum, :locnum, :ordnum)"),
                                    {'ingredients': ingredients, 'supnum': supnum, 'locnum': locnum,
                                     'ordnum': str(max_val+1)})
        db.session.commit()

        for ing in ingredients_list:
            result = db.session.execute(text("SELECT ingqty, ingmeasurementtype FROM ingredient WHERE ingnum = :ing AND locnum = :locnum "
                                             "AND supnum = :supnum"),
                                        {'ing': ing, 'locnum': locnum, 'supnum': supnum, })
            d = result_to_dict(result)
            if len(d) > 0:
                # update this row
                ingqty = int(d[0]['ingqty'])
                db.session.execute(text("UPDATE ingredient SET ingqty = :ingqty WHERE ingnum = :ingnum AND supnum = :supnum AND"
                                        " locnum = :locnum"),
                                   {'ingqty': ingqty+10,'ingnum': ing, 'supnum': supnum, 'locnum': locnum})
                db.session.commit()
            else:
                # add a new row
                db.session.execute(text("INSERT INTO ingredient (ingmeasurementtype, ingname, expdate, ingqty, ingnum,"
                                        " supnum, locnum) VALUES (:ingtype, :ingname, '12/7/24', '10', :num, :supnum, :locnum)"),
                                   {'ingtype': NUM_TO_TYPE[int(ing)], 'ingname': NUM_TO_ING[int(ing)], 'num': ing,
                                    'supnum': supnum, 'locnum': locnum})
                print('hello, inserting')
                db.session.commit()
        r = db.session.execute(text("SELECT * FROM ingredient"))
        print(r)
        print(r.fetchall())
        return '', 200
    except Exception as e:
        raise e
        return '', 500



def main():
    app.run(port=6969)
