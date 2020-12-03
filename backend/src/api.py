import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def drinks():
    drinks = [drink.short() for drink in Drink.query.all()]
    if len(drinks) == 0:
        abort(404)
    return jsonify({"success": True, "drinks": drinks}), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
def drinks_detail():
    drinks = [i.long() for i in Drink.query.all()]
    if len(drinks) == 0:
        abort(404)
    return jsonify({"success": True, "drinks": drinks}), 200


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@ requires_auth('post:drinks')
def create_drink():
    drink = request.get_json()['drink']
    created_drink = Drink(
        id=drink['id'], title=drink['title'], recipe=drink['recipe'])
    try:
        Drink.insert(created_drink)
    except:
        abort(404)
    return jsonify({"success": True,
                    "drinks": [{"id": drink['id'],
                                "title": drink['title'],
                                "recipe": drink['recipe']}]})


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@ requires_auth('patch:drinks')
def edit_drink(id):
    queried_drink = Drink.query.get(id)
    if queried_drink is None:
        abort(404)
    drink = request.get_json()['drink']
    print(drink)
    queried_drink.title = drink['title']
    queried_drink.recipe = drink['recipe']
    queried_drink.update()
    return jsonify({"success": True,
                    "drinks": {"title": drink['title'], "recipe": drink['recipe']}})


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@ app.route('/drinks/<int:id>', methods=['DELETE'])
@ requires_auth('delete:drinks')
def delete_drink(id):
    queried_drink = Drink.query.get(id)
    if queried_drink is None:
        abort(404)
    Drink.delete(queried_drink)
    return jsonify({"success": True, "delete": id})


# Error Handling
'''
Example error handling for unprocessable entity
'''


@ app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@ app.errorhandler(400)
def bad_request(code):
    return jsonify({
        "message": str(code),
        "code": 400
    })


@ app.errorhandler(401)
def unauthorize(code):
    return jsonify({
        "message": str(code),
        "code": 401
    })


@ app.errorhandler(403)
def forbidden(code):
    return jsonify({
        "message": str(code),
        "code": 403
    })


@ app.errorhandler(404)
def not_found(code):
    return jsonify({
        "message": str(code),
        "code": 404
    })


@ app.errorhandler(405)
def method_not_allowed(code):
    return jsonify({
        "message": str(code),
        "code": 405
    })


@ app.errorhandler(406)
def not_acceptable(code):
    return jsonify({
        "message": str(code),
        "code": 406
    })


@ app.errorhandler(408)
def request_timeout(code):
    return jsonify({
        "message": str(code),
        "code": 408
    })


@ app.errorhandler(409)
def conflict(code):
    return jsonify({
        "message": str(code),
        "code": 409
    })


@ app.errorhandler(410)
def gone(code):
    return jsonify({
        "message": str(code),
        "code": 410
    })


@ app.errorhandler(411)
def length_required(code):
    return jsonify({
        "message": str(code),
        "code": 411
    })


@ app.errorhandler(412)
def precondition_faled(code):
    return jsonify({
        "message": str(code),
        "code": 412
    })


@ app.errorhandler(413)
def not_processable(code):
    return jsonify({
        "message": str(code),
        "code": 413
    })


@ app.errorhandler(414)
def long_request(code):
    return jsonify({
        "message": str(code),
        "code": 414
    })


@ app.errorhandler(416)
def not_statisfiable(code):
    return jsonify({
        "message": str(code),
        "code": 416
    })


@ app.errorhandler(417)
def expectation_failed(code):
    return jsonify({
        "message": str(code),
        "code": 417
    })


@ app.errorhandler(418)
def teapot(code):
    return jsonify({
        "message": str(code),
        "code": 418
    })


@ app.errorhandler(422)
def processable(code):
    return jsonify({
        "message": str(code),
        "code": 422
    })


@ app.errorhandler(423)
def locked(code):
    return jsonify({
        "message": str(code),
        "code": 423
    })


@ app.errorhandler(424)
def dependency(code):
    return jsonify({
        "message": str(code),
        "code": 424
    })


@ app.errorhandler(429)
def too_many(code):
    return jsonify({
        "message": str(code),
        "code": 429
    })


@ app.errorhandler(431)
def not_large(code):
    return jsonify({
        "message": str(code),
        "code": 431
    })


@ app.errorhandler(451)
def leagal(code):
    return jsonify({
        "message": str(code),
        "code": 451
    })


@ app.errorhandler(500)
def serverError(code):
    return jsonify({
        "message": str(code),
        "code": 500
    })


@ app.errorhandler(501)
def not_implemented(code):
    return jsonify({
        "message": str(code),
        "code": 501
    })


@ app.errorhandler(502)
def gateway(code):
    return jsonify({
        "message": str(code),
        "code": 502
    })


@ app.errorhandler(503)
def service(code):
    return jsonify({
        "message": str(code),
        "code": 503
    })


@ app.errorhandler(504)
def timeout(code):
    return jsonify({
        "message": str(code),
        "code": 504
    })


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
