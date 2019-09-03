from flask import Flask, jsonify, request, Response
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
        return "False"
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


app.run(port=5000)
