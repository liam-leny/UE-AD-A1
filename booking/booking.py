from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res

@app.route("/bookings/<userid>", methods=['GET'])
def get_bookings_by_userid(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            res = make_response(jsonify(booking),200)
            return res
    return make_response(jsonify({"error":"User ID not found"}),400)

@app.route("/bookings/<userid>", methods=['POST'])
def add_booking(userid):
    req = request.get_json()
    validity = False
    userFound = False

    if 'date' not in req or 'movieid' not in req:
        return make_response(jsonify({"error":"Missing 'date' or 'movieid' in request"}), 400)
    
   # Check the validity of the booking by calling the external service showtimes
    showTimesReponse = requests.get('http://localhost:3202/showmovies/' + req["date"]).json()
    print(showTimesReponse)
    if req["movieid"] in showTimesReponse["movies"] :
         validity = True

    if not validity :
       return make_response(jsonify({"error":"The movie is not available on the requested date"}), 400)
        
    # Check if the user has an existing booking
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            userFound = True
            
            # Check if the user has already made a booking on the requested date
            dateFound = False
            for dateEntry in booking["dates"]:
                if dateEntry["date"] == req["date"]:
                    dateEntry["movies"].append(req["movieid"])
                    dateFound = True
            
            # If the user has never booked on this date, create a new entry
            if not dateFound:
                booking["dates"].append({
                    "date": req["date"],
                    "movies": [req["movieid"]]
                })

    # If the user has never made a booking, create a new user entry
    if not userFound:
        new_booking = {
            "userid": userid,
            "dates": [
                {
                    "date": req["date"],
                    "movies": [req["movieid"]]
                }
            ]
        }
        bookings.append(new_booking)

    write(bookings)
    res = make_response(jsonify({"message": "Booking added successfully"}), 200)
    return res

def write(bookings):
    data = {"bookings": bookings}
    with open('./databases/bookings.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
