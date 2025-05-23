# Import the Flask class from the flask module
from flask import Flask, make_response

# Create an instance of the Flask class, passing in the name of the current module
app = Flask(__name__)

# Define a route for the root URL ("/")
@app.route("/")
def index():
    # Function that handles requests to the root URL
    # Return a plain text response
    return "hello world"

@app.route("/no_content")
def no_content():
    # response = {"message": "No content found"}
    # return response, 204
    resp = make_response({"message": "No content found"})
    resp.status_code = 204
    # Function that handles requests to the root URL
    return resp
    
@app.route("/exp")
def index_explicit():
    resp = make_response({"message": "hello world"})
    resp.status_code = 200
    return resp

