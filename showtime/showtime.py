from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = "0.0.0.0"

with open('{}/showtime/databases/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]


@app.route("/", methods=["GET"])
def home():
    """
    Route for the home page of the Showtime service.
    Displays a simple welcome message.
    """
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


@app.route("/showtimes", methods=["GET"])
def get_json():
    """
    Route to get the complete showtime schedule.
    Returns the full schedule as a JSON response with a 200 status code.
    """
    res = make_response(jsonify(schedule), 200)
    return res


@app.route("/showmovies/<date>", methods=["GET"])
def get_shedule_by_date(date):
    """
    Route to get the showtime schedule for a specific date.
    Iterates through the schedule to find a matching date and returns the corresponding schedule.
    If no matching date is found, returns an error message with a 400 status code.
    """
    for oneSchedule in schedule:
        if str(oneSchedule["date"]) == str(date):
            res = make_response(jsonify(oneSchedule), 200)
            return res
    return make_response(jsonify({"error": "Date not found"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
