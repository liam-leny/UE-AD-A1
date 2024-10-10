from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]

# URLs for the other services
BOOKING_SERVICE_URL = 'http://localhost:3201'
MOVIE_SERVICE_URL = 'http://localhost:3200'

@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"

# Get user reservations
@app.route("/users/<userId>/reservations", methods=['GET'])
def get_user_reservations(userId):
   
    user = next((user for user in users if user["id"] == userId), None)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    booking_url = f"{BOOKING_SERVICE_URL}/bookings/{userId}"
    bookings_response = requests.get(booking_url)
    
    if bookings_response.status_code == 200:
        return make_response(bookings_response.json(), 200)
    else:
        return make_response(jsonify({"error": "Could not retrieve bookings"}), 500)
  
# Get user movies   
@app.route("/users/<userId>/movies", methods=['GET'])
def get_user_movies(userId):
   
    reservations_response = get_user_reservations(userId)

    if reservations_response.status_code != 200:
        return reservations_response
     
    bookings = reservations_response.get_json().get("dates", [])
    
    movie_details = []
    for booking in bookings:
        for movie_id in booking["movies"]:
            # Call the Movie service for each reserved movie
            movie_url = f"{MOVIE_SERVICE_URL}/movies/{movie_id}"
            movie_response = requests.get(movie_url)
            if movie_response.status_code == 200:
                movie_details.append(movie_response.json())
    
    if movie_details:
        return make_response(jsonify({"userId": userId, "movies": movie_details}), 200)
    else:
        return make_response(jsonify({"error": "No movies found"}), 404)

# Check reservation availability
@app.route("/users/<userId>/reservations/availability", methods=['POST'])
def check_availability(userId):
   
    user = next((user for user in users if user["id"] == userId), None)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    req = request.get_json()
    if 'date' not in req or 'movieid' not in req:
        return make_response(jsonify({"error":"Missing 'date' or 'movieid' in request"}), 400)

    booking_url = f"{BOOKING_SERVICE_URL}/bookings/{userId}"
    availability_check = requests.post(booking_url, json=req)

    if availability_check.status_code == 200:
        return make_response(availability_check.json(), 200)
    else:
        return make_response(availability_check.json(), availability_check.status_code)

# Update user info
@app.route("/users/<userId>", methods=['PUT'])
def update_user(userId):
    user = next((user for user in users if user["id"] == userId), None)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    data = request.json
    if not data:
        return make_response(jsonify({"error": "No data provided"}), 400)

    user.update(data)
    return make_response(jsonify(user), 200)

# Delete user
@app.route("/users/<userId>", methods=['DELETE'])
def delete_user(userId):
    global users
    user = next((user for user in users if user["id"] == userId), None)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    users = [u for u in users if u["id"] != userId]
    return make_response(jsonify({"message": "User deleted"}), 200)


if __name__ == "__main__":
    print("Server running on port %s" % PORT)
    app.run(host=HOST, port=PORT)
