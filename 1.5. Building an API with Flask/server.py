# Import the Flask class from the flask module
from flask import Flask, make_response, request

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

data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]

@app.route("/data")
def get_data():
    try:
        # Check if 'data' exists and has a length greater than 0
        if data and len(data) > 0:
            # Return a JSON response with a message indicating the length of the data
            return {"message": f"Data of length {len(data)} found"}
        else:
            # If 'data' is empty, return a JSON response with a 500 Internal Server Error status code
            return {"message": "Data is empty"}, 500
    except NameError:
        # Handle the case where 'data' is not defined
        # Return a JSON response with a 404 Not Found status code
        return {"message": "Data not found"}, 404
    
@app.route("/name_search")
def name_search():
    query = request.args.get('q')
    if query is None:
        return {"message": "Query parameter 'q' is missing"}, 400
    
    if query.strip() == "" or query.isdigit():
        return {"message": "Query parameter 'q' is invalid"}, 422
    
    for person in data:
        if person['first_name'].lower() == query.lower():
            return person, 200
        
    return {"message": "Person not found"}, 404

@app.get("/count")
def count():
    try:
        return {"data count": len(data)}, 200
    except NameError:
        return {"message": "data not defined"}, 500

@app.get("/person/<uuid>")
def find_by_uuid(uuid):
    if uuid is None:
        return {"message": "uuid parameter is missing"}, 400

    if uuid.strip() == "":
        return {"message": "uuid parameter is invalid"}, 422

    for person in data:
        if person['id'] == uuid:
            return person, 200

    return {"message": "Person not found"}, 404

@app.route("/person/<uuid>", methods=['DELETE'])
def delete_person(uuid):
    if uuid is None:
        return {"message": "uuid parameter is missing"}, 400
    
    if uuid.strip() == "":
        return {"message": "uuid parameter is invalid"}, 422

    for person in data:
        if person['id'] == str(uuid):
            data.remove(person)
            return {"message": "Person deleted with ID " + uuid}, 200

    return {"message": "Person not found"}, 404


@app.route("/person", methods=['POST'])
def add_by_uuid():
    new_person = request.get_json()
    
    if not new_person:
         return {"message": "Invalid input, no data provided"}, 422
    try:
        data.append(new_person)
    except NameError:
        return {"message": "data not defined"}, 500

    return {"message": "Person created successfully with ID " + new_person['id']}, 200

@app.errorhandler(404)
def api_not_found(error):
    return {"message": "{API not found}"}, 404