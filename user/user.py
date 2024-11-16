from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

PORT = 3203
HOST = "0.0.0.0"

with open("{}/databases/users.json".format("."), "r") as jsf:
    users = json.load(jsf)["users"]

# URLs for the other services
BOOKING_SERVICE_URL = "http://localhost:3201"
MOVIE_SERVICE_URL = "http://localhost:3200"


@app.route("/", methods=["GET"])
def home():
    """
    Route for the home page of the User service
    """
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


# Get user reservations
@app.route("/users/<userId>/reservations", methods=["GET"])
def get_user_reservations(userId):
    """
    Route to get all reservations for a specific user.
    Checks if the user exists and calls the Booking service to get the reservations.
    Returns booking data if found, otherwise returns an error.
    """
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
@app.route("/users/<userId>/movies", methods=["GET"])
def get_user_movies(userId):
    """
    Route to get movie details for a specific user's reservations.
    Calls get_user_reservations to retrieve the reservations and then queries the Movie service for each movie.
    Returns a list of movie details or an error if no movies are found.
    """
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
@app.route("/users/<userId>/reservations/availability", methods=["POST"])
def check_availability(userId):
    """
    Route to check the availability of a reservation for a specific user.
    Validates the user's existence and checks if the 'date' and 'movieid' are provided in the request body.
    Forwards the availability request to the Booking service and returns the response.
    """
    user = next((user for user in users if user["id"] == userId), None)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    req = request.get_json()
    if "date" not in req or "movieid" not in req:
        return make_response(
            jsonify({"error": "Missing 'date' or 'movieid' in request"}), 400
        )

    booking_url = f"{BOOKING_SERVICE_URL}/bookings/{userId}"
    availability_check = requests.post(booking_url, json=req)

    if availability_check.status_code == 200:
        return make_response(availability_check.json(), 200)
    else:
        return make_response(availability_check.json(), availability_check.status_code)


# Update user info
@app.route("/users/<userId>", methods=["PUT"])
def update_user(userId):
    """
    Route to update user information.
    Checks if the user exists and validates that data is provided in the request body.
    Updates the user's information and returns the updated data.
    """
    user = next((user for user in users if user["id"] == userId), None)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    data = request.json
    if not data:
        return make_response(jsonify({"error": "No data provided"}), 400)

    user.update(data)
    return make_response(jsonify(user), 200)


# Delete user
@app.route("/users/<userId>", methods=["DELETE"])
def delete_user(userId):
    """
    Route to delete a user.
    Checks if the user exists, removes them from the users list, and returns a success message.
    """
    global users
    user = next((user for user in users if user["id"] == userId), None)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    users = [u for u in users if u["id"] != userId]
    return make_response(jsonify({"message": "User deleted"}), 200)


if __name__ == "__main__":
    print("Server running on port %s" % PORT)
    app.run(host=HOST, port=PORT)
