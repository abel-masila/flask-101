from flask import Flask, jsonify, request, Response
import json
from settings import *
import jwt
import datetime

from BookModal import *

app.config['SECRET_KEY'] = "admin"


# Default route
@app.route("/")
def helloworld():
    return "Hello World"


@app.route("/login")
def get_token():
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
    token = jwt.encode({'exp': expiration_date},
                       app.config['SECRET_KEY'], algorithm='HS256')
    return token
# GET /books
@app.route("/books", methods=['GET'])
def get_books():
    token = request.args.get('token')
    try:
        jwt.decode(token, app.config['SECRET_KEY'])
    except:
        return jsonify({'error': 'Invalid token supplied'})
    return jsonify({'books': Book.get_all_books()})


# sanitize user request
def validBookObj(bookObj):
    if ("name" in bookObj and "price" in bookObj and "isbn" in bookObj):
        return True
    else:
        return False

# POST /books
@app.route("/books", methods=['POST'])
def add_books():
    data = request.get_json()
    if (validBookObj(data)):

        Book.add_book(data["name"], data["price"], data["isbn"])
        response = Response("", 201, mimetype="application/json")
        response.headers["Location"] = "/books/" + str(data["isbn"])
        return response

    else:
        invalidBookObjErrorResponse = {
            "error": "Invalid book object passed.",
            "helpString": "Data passed in similar format to this {'name': 'js for dummies','isbn': 122343,'price': 3423}"
        }
        response = Response(json.dumps(invalidBookObjErrorResponse),
                            status=400, mimetype="application/json")
        return response


# GET /books/ISBN
@app.route("/books/<int:isbn>")
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)


def validPutBookObj(bookObj):
    if ("name" in bookObj and "price" in bookObj):
        return True
    else:
        return False
# PUT /books/ISBN -this requires user to send all the details about the entity
@app.route("/books/<int:isbn>", methods=["PUT"])
def replace_book(isbn):
    data = request.get_json()
    if (not validPutBookObj(data)):
        invalidBookObjErrorResponse = {
            "error": "Valid book object must be passed in the request.",
            "helpString": "Data passed in similar format to this {'name': 'js for dummies','price': 3423}"
        }
        response = Response(json.dumps(invalidBookObjErrorResponse),
                            status=400, mimetype="application/json")
        return response

    Book.replace_book(isbn, data["name"], data["price"])
    response = Response("", status=204)
    return response

# PATCH /books/ISBN
@app.route("/books/<int:isbn>", methods=["PATCH"])
def update_book(isbn):
    data = request.get_json()
    if ("name" in data):
        Book.update_book_name(isbn, data['name'])
    if ("price" in data):
        Book.update_book_price(isbn, data['price'])

    response = Response("", status=204)
    response.headers["Location"] = "/books/" + str(isbn)
    return response

# DELETE /books/ISBN
@app.route("/books/<int:isbn>", methods=["DELETE"])
def delete_book(isbn):
    if (Book.delete_book(isbn)):
        return Response("", status=204)
    errorMsg = {
        "error": "Book with th ISBN number provided was not found"
    }
    return Response(json.dumps(errorMsg), status=404, mimetype="application/json")


app.run(port=5000)
