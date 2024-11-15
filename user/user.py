# REST API
from flask import Flask, request, jsonify, make_response
from ariadne import QueryType
import requests
import json
from werkzeug.exceptions import NotFound

# CALLING gRPC requests
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc

# CALLING GraphQL requests


app = Flask(__name__)

PORT = 3004
HOST = "0.0.0.0"

with open("{}/data/users.json".format("."), "r") as jsf:
    users = json.load(jsf)["users"]


# Function to create a gRPC stub to interact with the Booking service
def get_booking_stub():
    channel = grpc.insecure_channel("localhost:3201")
    return booking_pb2_grpc.BookingStub(channel)


@app.route("/", methods=["GET"])
def home():
    """
    The home route for the User service.
    This route returns a simple welcome message when accessed.
    """
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


# Get user reservations
@app.route("/users/<userId>/reservations", methods=["GET"])
def get_user_reservations(userId):
    """
    This route handles the request to get all reservations for a specific user by their userId.
    It fetches user data from the loaded `users` list and calls the Booking service to get the reservations.
    """
    user = next((user for user in users if user["id"] == userId), None)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    stub = get_booking_stub()
    try:
        request = booking_pb2.UserID(userid=userId)
        response = stub.GetBookingByUserID(request)
        response_data = {
            "userId": userId,
            "dates": [
                {"date": date_entry.date, "movies": list(date_entry.movies)}
                for date_entry in response.dates
            ],
        }

        return make_response(jsonify(response_data), 200)
    except grpc.RpcError as e:
        return make_response(
            jsonify({"error": f"Error contacting Booking service: {e.details()}"}), 500
        )


# Get user movies
@app.route("/users/<userId>/movies", methods=["GET"])
def get_user_movies(userId):
    """
    This route handles the request to get all movies associated with a user's reservations.
    It first retrieves the user's reservations and then fetches movie details using the Movie service via GraphQL.
    """
    reservations_response = get_user_reservations(userId)

    if reservations_response.status_code != 200:
        return reservations_response

    bookings = reservations_response.get_json().get("dates", [])

    movie_details = []
    for booking in bookings:
        for movie_id in booking["movies"]:
            # Call the Movie service for each reserved movie
            query = (
                '''
               query{
                  movie_with_id(_id:"'''
                + movie_id
                + """") {
                     title
                     rating
                     actors{
                        firstname
                        lastname
                        birthyear
                     }
                  }
               }
            """
            )
            movie_response = requests.post(
                "http://127.0.0.1:3001/graphql", json={"query": query}
            )
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
    This route allows users to check the availability of a reservation for a specific date and movie.
    It sends a request to the Booking service to check if a reservation can be made.
    """
    user = next((user for user in users if user["id"] == userId), None)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    req = request.get_json()
    if (
        "date" not in req or "movieid" not in req
    ):  # Problème probable avec 'movieid' au lieu de 'id'
        return make_response(
            jsonify({"error": "Missing 'date' or 'movieid' in request"}), 400
        )

    # Verify the availability
    stub = get_booking_stub()
    try:
        booking_request = booking_pb2.BookingRequest(
            userid=userId, date=req["date"], movieid=req["movieid"]
        )
        response = stub.AddBooking(booking_request)
        return make_response(
            jsonify({"message": response.message, "error": response.error}), 200
        )
    except grpc.RpcError as e:
        return make_response(
            jsonify({"error": f"Error contacting Booking service: {e.details()}"}), 500
        )


# Update user info
@app.route("/users/<userId>", methods=["PUT"])
def update_user(userId):
    """
    This route allows for updating a user's information. It takes a PUT request with the updated user data.
    If the user is found, their data will be updated, and the new data will be returned.
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
    This route deletes a user by their userId. It removes the user from the loaded users list.
    If the user is not found, it returns an error.
    """
    global users
    user = next((user for user in users if user["id"] == userId), None)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    users = [u for u in users if u["id"] != userId]
    return make_response(jsonify({"message": "User deleted"}), 200)


if __name__ == "__main__":
    print("Server running on port %s" % PORT)
    app.run(host=HOST, port=PORT, debug=True)
