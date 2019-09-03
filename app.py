from flask import Flask
app = Flask(__name__)


# Default route
@app.route("/")
def helloworld():
    return "Hello World"


app.run(port=5000)
