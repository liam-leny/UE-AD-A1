from ariadne import (
    graphql_sync,
    make_executable_schema,
    load_schema_from_path,
    ObjectType,
    QueryType,
    MutationType,
)
from flask import Flask, make_response, request, jsonify, render_template

import resolvers as r

PORT = 3200
HOST = "0.0.0.0"
app = Flask(__name__)

type_defs = load_schema_from_path("movie/movie.graphql")
movie = ObjectType("Movie")

query = QueryType()
query.set_field("home", r.resolve_home)
query.set_field("all_movies", r.all_movies)
query.set_field("movie_with_id", r.movie_with_id)
query.set_field("movie_with_title", r.movie_with_title)
query.set_field("movie_with_director", r.movie_with_director)
query.set_field("movie_with_rating", r.movie_with_rating)

mutation = MutationType()
mutation.set_field("update_movie_rate", r.update_movie_rate)
mutation.set_field("add_movie", r.add_movie)
mutation.set_field("delete_movie", r.delete_movie)

actor = ObjectType("Actor")
movie.set_field("actors", r.resolve_actors_in_movie)
schema = make_executable_schema(type_defs, movie, query, mutation, actor)


@app.route("/graphql", methods=["POST"])
def graphql_server():
    """
    The '/graphql' route is the entry point for GraphQL queries and mutations.
    It accepts POST requests containing the query or mutation data in JSON format,
    executes it and returns the results.
    """
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=None, debug=app.debug)
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT, debug=True)
