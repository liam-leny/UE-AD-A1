from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]
   

BOOKING_SERVICE_URL = 'http://localhost:3201'
MOVIE_SERVICE_URL = 'http://localhost:3200'


@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

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


@app.route("/users/<userId>/movies", methods=['GET'])
def get_user_movies(userId):
   
   # user = next((user for user in users if user["id"] == userId), None)
   # if not user:
   #     return make_response(jsonify({"error": "User not found"}), 404)

   # booking_url = f"{BOOKING_SERVICE_URL}/bookings/{userId}"
   # bookings_response = requests.get(booking_url)

   # if bookings_response.status_code != 200:
   #     return make_response(jsonify({"error": "Could not retrieve bookings"}), 500)

   # bookings = bookings_response.json().get("dates", [])
   
   reservations_response = get_user_reservations(userId)

   # Check if there is an error in reservations_response
   if reservations_response.status_code != 200:
       return reservations_response 

   bookings = reservations_response.get_json().get("dates", [])
   
   # For each movie reserved by the user, fetch the movie details from the movie service
   movie_details = []
   for booking in bookings:
       for movie_id in booking["movies"]:
           movie_url = f"{MOVIE_SERVICE_URL}/movies/{movie_id}"
           movie_response = requests.get(movie_url)
           if movie_response.status_code == 200:
               movie_details.append(movie_response.json())
   
   if movie_details:
       return make_response(jsonify({"userId": userId, "movies": movie_details}), 200)
   else:
       return make_response(jsonify({"error": "No movies found"}), 404)
    
    
    
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
