import json
import os


# Load movies from a JSON file
def load_movies():
    """
    Loads the list of movies from a JSON file.
    Returns:
        A list of movies (list of dictionaries).
    """
    with open("{}/movie/data/movies.json".format("."), "r") as file:
        return json.load(file)["movies"]


# Write movies to a JSON file
def write(movies):
    """
    Writes the updated list of movies back to the JSON file.
    Args:
        movies (list): List of movie dictionaries to be saved.
    """
    with open("{}/movie/data/movies.json".format("."), "w") as file:
        json.dump({"movies": movies}, file, indent=4)


# Resolver for the 'home' query
def resolve_home(_, info):
    """
    Resolver for the 'home' query.
    Returns a simple welcome message as a string.
    """
    return "<h1 style='color:blue'>Welcome to the Movie service!</h1>"


# Query resolver to fetch all movies
def all_movies(_, info):
    """
    Resolver for the 'all_movies' query.
    Returns:
        The entire list of movies.
    """
    return load_movies()


# Query resolver to fetch a movie by its ID
def movie_with_id(_, info, _id):
    """
    Resolver for the 'movie_with_id' query.
    Finds and returns a movie by its unique ID.
    Args:
        _id (str): The ID of the movie to search for.
    Returns:
        The matching movie dictionary or None if not found.
    """
    movies = load_movies()
    for movie in movies:
        if movie["id"] == _id:
            return movie
    return None


# Query resolver to fetch movies by title
def movie_with_title(_, info, _title):
    """
    Resolver for the 'movie_with_title' query.
    Finds and returns all movies that match the given title.
    Args:
        _title (str): The title of the movie(s) to search for.
    Returns:
        A list of movies with the specified title.
    """
    movies = load_movies()
    return [movie for movie in movies if movie["title"] == _title]


# Query resolver to fetch movies by director
def movie_with_director(_, info, _director):
    """
    Resolver for the 'movie_with_director' query.
    Finds and returns all movies directed by a specific director.
    Args:
        _director (str): The name of the director (case-insensitive).
    Returns:
        A list of movies directed by the specified director.
    """
    movies = load_movies()
    return [movie for movie in movies if movie["director"].lower() == _director.lower()]


# Query resolver to fetch movies by rating
def movie_with_rating(_, info, _rating):
    """
    Resolver for the 'movie_with_rating' query.
    Finds and returns all movies with a rating greater than or equal to the specified value.
    Args:
        _rating (float): The minimum rating (must be between 0 and 10).
    Returns:
        A list of movies with the required rating.
    Raises:
        Exception: If the rating is outside the range 0-10.
    """
    movies = load_movies()
    if _rating < 0 or _rating > 10:
        raise Exception("Rating must be between 0 and 10")
    return [movie for movie in movies if movie["rating"] >= _rating]


# Resolver to fetch actors for a specific movie
def resolve_actors_in_movie(movie, info):
    """
    Resolver for fetching actors associated with a specific movie.
    Args:
        movie (dict): The movie object whose actors need to be fetched.
    Returns:
        A list of actors appearing in the movie.
    """
    with open("{}/movie/data/actors.json".format("."), "r") as file:
        actors = json.load(file)
    return [actor for actor in actors["actors"] if movie["id"] in actor["films"]]


# Mutation resolver to update a movie's rating
def update_movie_rate(_, info, _id, _rate):
    """
    Resolver for the 'update_movie_rate' mutation.
    Updates the rating of a specific movie by its ID.
    Args:
        _id (str): The ID of the movie to update.
        _rate (float): The new rating for the movie.
    Returns:
        The updated movie dictionary.
    Raises:
        Exception: If the movie ID is not found.
    """
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
        raise Exception("Movie ID not found")


# Mutation resolver to add a new movie
def add_movie(_, info, movie_input):
    """
    Resolver for the 'add_movie' mutation.
    Adds a new movie to the collection.
    Args:
        movie_input (dict): A dictionary containing the movie's details.
    Returns:
        The newly added movie dictionary.
    Raises:
        Exception: If a movie with the same ID already exists.
    """
    movies = load_movies()

    for movie in movies:
        if movie["id"] == movie_input["id"]:
            raise Exception("Movie ID already exists")

    new_movie = {
        "title": movie_input["title"],
        "rating": movie_input["rating"],
        "director": movie_input["director"],
        "id": movie_input["id"],
    }

    movies.append(new_movie)
    write(movies)
    return new_movie


# Mutation resolver to delete a movie by ID
def delete_movie(_, info, _id):
    """
    Resolver for the 'delete_movie' mutation.
    Deletes a movie from the collection by its ID.
    Args:
        _id (str): The ID of the movie to delete.
    Returns:
        The deleted movie dictionary.
    Raises:
        Exception: If the movie with the specified ID does not exist.
    """
    movies = load_movies()

    movie_to_delete = None
    for movie in movies:
        if movie["id"] == _id:
            movie_to_delete = movie
            break

    if not movie_to_delete:
        raise Exception("The movie with this ID does not exist.")

    movies.remove(movie_to_delete)
    write(movies)
    return movie_to_delete
