from flask import Flask, render_template, request
import tmdb_client
from waitress import serve

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def homepage():
    selected_list = request.args.get('list_type', "popular")
    movies_lists = ["top_rated", "upcoming", "popular", "now_playing"]
    list_type = selected_list
    if selected_list in movies_lists:
        movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    else:
        selected_list = "popular"
        movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list, movies_lists=movies_lists)


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
   details = tmdb_client.get_single_movie(movie_id)
   cast = tmdb_client.get_single_movie_cast(movie_id)
   return render_template("movie_details.html", movie=details, cast=cast)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


#if __name__ == "__main__":
#    app.run(debug=True)

if __name__ == "__main__":
    #app.run('0.0.0.0',port=server_port)
    serve(app)