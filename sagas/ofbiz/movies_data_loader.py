import fire

from sagas.ofbiz.builder import oc, finder, desc_model, abbrev
from json_utils import read_json_file
import sagas.ofbiz
import os

Long = oc.gateway.jvm.Long
ValueHelper=oc.gateway.jvm.com.sagas.generic.ValueHelper

# helper functions
def indicator(val):
    return 'Y' if val else 'N'

def create_or_store(entity, movie):
    val = oc.delegator.makeValue(entity)
    val.set("movieId", str(movie["id"]))
    # val.set("voteCount", movie['vote_count'])
    ValueHelper.setNumericValue(val, "voteCount", movie['vote_count'])
    # ValueHelper.setNumericValue(val, "voteAverage", movie['vote_average'])
    val.set('voteAverage', float(movie['vote_average']))
    val.set('video', indicator(movie['video']))
    val.set('title', movie['title'])
    val.set('popularity', movie['popularity'])
    val.set('posterPath', movie['poster_path'])
    val.set('overview', abbrev(movie['overview'], 250))
    # val.set('releaseDate', movie['release_date'])
    ValueHelper.setDate(val, "releaseDate", movie['release_date'])

    return oc.delegator.createOrStore(val)


def store_movie_genres(genre):
    val = oc.delegator.makeValue("SaMovieGenres")
    val.set("movieGenresId", str(genre["id"]))
    val.set("movieGenresName", genre["name"])
    return oc.delegator.createOrStore(val)


def set_movie_genres(movie_id, genre_ids):
    for gid in genre_ids:
        val = oc.delegator.makeValue("SaMovieGenresAppl")
        val.set("movieId", str(movie_id))
        val.set("movieGenresId", str(gid))
        oc.delegator.createOrStore(val)

root_dir=os.path.dirname(sagas.ofbiz.__file__).replace("sagas/ofbiz","")

def genres_loader():
    genres_root = read_json_file(root_dir + "data/movie_genres_f.json")

    genres_map = {}
    for genre in genres_root['genres']:
        genres_map[genre['id']] = genre['name']

    for genre in genres_root['genres']:
        store_movie_genres(genre)

def movies_loader(file):
    data_root=read_json_file(file)

    print(data_root["page"], "/", data_root["total_pages"])
    movies=data_root["results"]

    for movie in movies:
        result = create_or_store("SaMovie", movie)
        set_movie_genres(movie["id"], movie['genre_ids'])
        print(result.get("title"))

class MoviesDataLoader(object):
    def load_all(self):
        genres_loader()

        ## load seed file from 1-10
        for i in range(1,11):
            print(".. load seeds", i)
            seed_file=root_dir + "data/movies_{}.json".format(i)
            movies_loader(seed_file)

if __name__ == '__main__':
    # fire.Fire(MoviesDataLoader)
    MoviesDataLoader().load_all()

