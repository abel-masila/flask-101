from flask import Flask, jsonify, request, Response
import json
app = Flask(__name__)

books = [
    {
        'name': 'Java for dummies',
        'price': 799,
        'isbn': 343434
    },
    {
        'name': 'C# for dummies',
        'price': 699,
        'isbn': 343433
    }
]

# Default route
@app.route("/")
def helloworld():
    return "Hello World"


# GET /books
@app.route("/books", methods=['GET'])
def get_books():
    return jsonify({'books': books})


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
        new_book = {
            "name": data["name"],
            "price": data["price"],
            "isbn": data["isbn"]
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype="application/json")
        response.headers["Location"] = "/books/" + str(new_book["isbn"])
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
    return_value = {}
    for book in books:
        if (book['isbn'] == isbn):
            return_value = {
                'name': book['name'],
                'isbn': book['isbn'],
                'price': book['price']
            }
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

    new_book = {
        "name": data["name"],
        "price": data["price"],
        "isbn": isbn
    }
    i = 0
    for book in books:
        currentIsbn = book["isbn"]
        if (currentIsbn == isbn):
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response

# PATCH /books/ISBN
@app.route("/books/<int:isbn>", methods=["PATCH"])
def update_book(isbn):
    data = request.get_json()
    updated_book = {}
    if ("name" in data):
        updated_book["name"] = data["name"]
    if ("price" in data):
        updated_book["price"] = data["price"]
    for book in books:
        if (book["isbn"] == isbn):
            book.update(updated_book)
    response = Response("", status=204)
    response.headers["Location"] = "/books/" + str(isbn)
    return response


app.run(port=5000)
