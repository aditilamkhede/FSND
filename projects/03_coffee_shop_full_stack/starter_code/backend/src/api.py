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
# db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where
        drinks is the list of drinks or appropriate status code indicating
        reason for failure
'''
@app.route('/drinks')
def drinks():
    # print("In Drinks")
    try:
        drinks = Drink.query.all()
        # print("DRINKS", drinks)
        drnks = [Drink.short() for Drink in drinks]
    except Exception as e:
        abort(404)

    return jsonify({
            "success": True,
            "drinks": drnks
            })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where
        drinks is the list of drinks or appropriate status code indicating
        reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    print("In Drinks Details")
    try:
        drinks = Drink.query.all()
        drnks = [Drink.long() for Drink in drinks]
    except Exception as e:
        abort(404)

    return jsonify({
            "success": True,
            "drinks": drnks
            })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink or
        appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    # print("In Create Drink")
    try:
        body = request.get_json()
        # print("body", body)
        req_title = body.get('title', None)
        req_recipe = body.get('recipe', None)
        drink = Drink(title=req_title, recipe=json.dumps(req_recipe))
        drink.insert()

    except Exception as e:
        # print(str(e))
        abort(404)

    return jsonify({
            "success": True,
            "drinks": drink.long()
            })


# '''
# @TODO implement endpoint
#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where
#         drink an array containing only the updated drink or appropriate status
#         code indicating reason for failure
# '''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(payload, drink_id):
    try:
        body = request.get_json()
        req_title = body.get('title', None)
        req_recipe = body.get('recipe', None)

        # print('title', req_title)
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            raise AuthError('Drink id not found.', status_code=404)

        if req_title:
            drink.title = req_title
        if req_recipe:
            drink.recipe = json.dumps(req_recipe)
        drink.update()
    except Exception as e:
        raise

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is
        the id of the deleted record or appropriate status code indicating
        reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        # print("drink", len(drink))
        if drink is None:
            raise AuthError('Drink id not found.', status_code=404)

        drink.delete()
    except Exception as e:
        raise
        # AuthError(str(e), status_code=404)

    return jsonify({
        'success': True,
        'delete': drink.id
    })


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
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
@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method not allowed, check URL.'
    }), 405


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request.'
    }), 400


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error. Server encountered an error.'
    }), 500


# '''
# @TODO implement error handler for 404
#     error handler should conform to general task above
# '''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
           "success": False,
           "error": 404,
           "message": "resource not found"
           }), 404


# '''
# @TODO implement error handler for AuthError
#     error handler should conform to general task above
# '''
@app.errorhandler(AuthError)
def auth_error(error):
    # return jsonify({
    #     'success': False,
    #     'error': error.status_code,
    #     'message': error.to_dict()
    # })
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
