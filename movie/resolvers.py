import json
import os


def load_movies():
    with open("{}/movie/data/movies.json".format("."), "r") as file:
        return json.load(file)["movies"]


def write(movies):
    with open("{}/movie/data/movies.json".format("."), "w") as file:
        json.dump({"movies": movies}, file, indent=4)


def all_movies(_, info):
    return load_movies()


def movie_with_id(_, info, _id):
    movies = load_movies()
    for movie in movies:
        if movie["id"] == _id:
            return movie
    return None


def movie_with_title(_, info, _title):
    movies = load_movies()
    return [movie for movie in movies if movie["title"] == _title]


def movie_with_director(_, info, _director):
    movies = load_movies()
    return [movie for movie in movies if movie["director"].lower() == _director.lower()]


def movie_with_rating(_, info, _rating):
    movies = load_movies()
    if _rating < 0 or _rating > 10:
        raise Exception("Rating must be between 0 and 10")
    return [movie for movie in movies if movie["rating"] >= _rating]


def resolve_actors_in_movie(movie, info):
    with open("{}/movie/data/actors.json".format("."), "r") as file:
        actors = json.load(file)
    return [actor for actor in actors["actors"] if movie["id"] in actor["films"]]


def update_movie_rate(_, info, _id, _rate):
    movies = load_movies()
    updated_movie = None
    for movie in movies:
        if movie["id"] == _id:
            movie["rating"] = _rate
            updated_movie = movie

    if updated_movie:
        write(movies)
        return updated_movie
    else:
        raise Exception("movie ID not found")


def add_movie(_, info, movie_input):
    movies = load_movies()

    for movie in movies:
        if movie["id"] == movie_input["id"]:
            raise Exception("movie ID already exists")

    new_movie = {
        "title": movie_input["title"],
        "rating": movie_input["rating"],
        "director": movie_input["director"],
        "id": movie_input["id"],
    }

    movies.append(new_movie)
    write(movies)
    return new_movie


def delete_movie(_, info, _id):
    movies = load_movies()

    movie_to_delete = None
    for movie in movies:
        if movie["id"] == _id:
            movie_to_delete = movie
            break

    if not movie_to_delete:
        raise Exception("Le film avec cet ID n'existe pas.")

    movies.remove(movie_to_delete)
    write(movies)
    return movie_to_delete
