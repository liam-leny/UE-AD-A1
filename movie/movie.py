from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

with open('{}/databases/movies.json'.format("."), 'r') as jsf:
   movies = json.load(jsf)["movies"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'),200)

@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie),200)
            return res
    return make_response(jsonify({"error":"Movie ID not found"}),400)

@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie

    if not json:
        res = make_response(jsonify({"error":"movie title not found"}),400)
    else:
        res = make_response(jsonify(json),200)
    return res

@app.route("/moviesbydirector", methods=['GET'])
def get_movies_bydirector():
    json= ""
    if request.args:
        director = request.args.get("director")
        json = [movie for movie in movies if movie["director"].lower() == director.lower()]

        if json:
            return make_response(jsonify(json), 200)
        else:
            return make_response(jsonify({"error": "No movies found for the given director"}), 400)
    return make_response(jsonify({"error": "Director parameter is required"}), 400)

@app.route("/moviesbyrating", methods=['GET'])
def get_movies_byrating():
    json=""
    if request.args:
        try:
            rating = int(request.args.get("rating"))
            if rating < 0 or rating > 10:
                return make_response(jsonify({"error": "Rating must be between 0 and 10"}), 400)
            
            json = [movie for movie in movies if movie["rating"] >= rating]

            if json:
                return make_response(jsonify(json), 200)
            else:
                return make_response(jsonify({"error": "No movies found with the given rating or higher"}), 400)
        except ValueError:
            return make_response(jsonify({"error": "Invalid rating value"}), 400)
    return make_response(jsonify({"error": "Rating parameter is required"}), 400)

@app.route("/addmovie/<movieid>", methods=['POST'])
def add_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"}),409)

    movies.append(req)
    write(movies)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res


def write(movies):
    data = {"movies": movies}
    with open('./databases/movies.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie),200)
            return res

    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res

@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie),200)

    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res

@app.route("/help", methods=['GET'])
def get_help():
    endpoints = [
        {"path": "/", "method": "GET", "description": "Home page of the service"},
        {"path": "/template", "method": "GET", "description": "HTML template for Movie service"},
        {"path": "/json", "method": "GET", "description": "Get the full JSON database"},
        {"path": "/movies/<movieid>", "method": "GET", "description": "Get a movie by its id"},
        {"path": "/movies/<movieid>", "method": "POST", "description": "Add a movie by its id"},
        {"path": "/movies/<movieid>", "method": "DELETE", "description": "Delete a movie by its id"},
        {"path": "/moviesbytitle", "method": "GET", "description": "Get a movie by its title"},
        {"path": "/moviesbydirector", "method": "GET", "description": "Get movies by director"},
        {"path": "/moviesbyrating", "method": "GET", "description": "Get movies by rating"},
        {"path": "/movies/<movieid>/<rate>", "method": "PUT", "description": "Update a movie rate"},
        {"path": "/help", "method": "GET", "description": "List all available endpoints"},
    ]
    return make_response(jsonify({"endpoints": endpoints}), 200)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT, debug=True)