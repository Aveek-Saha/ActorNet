import urllib
import urllib.request
import urllib.parse
from unidecode import unidecode

import json
import os

import config

DATA_DIR = "data"
MOVIE_DIR = "{}/{}".format(DATA_DIR, "movies")

TMDB_ACTOR_URL = "https://api.themoviedb.org/3/search/person?api_key=%s&language=en-US&query=%s&page=1"
TMDB_CREDITS_URL = "https://api.themoviedb.org/3/person/%s/combined_credits?api_key=%s&language=en-US"

tmdb_api_key = config.tmdb_api_key


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def is_folder_exists(folder_name):
    return os.path.exists(folder_name)


def get_actor_id(name):

    url = TMDB_ACTOR_URL % (tmdb_api_key, urllib.parse.quote(name))
    response = urllib.request.urlopen(url)
    res_data = response.read()
    jres = json.loads(res_data)

    if jres['total_results'] > 0:
        actor = jres['results'][0]
        return actor['id']
    else:
        return -1


def get_actor_credits(actor_id):

    url = TMDB_CREDITS_URL % (urllib.parse.quote(str(actor_id)), tmdb_api_key)
    response = urllib.request.urlopen(url)
    res_data = response.read()
    jres = json.loads(res_data)

    credits = jres['cast']

    for credit in credits:
        json.dump(credit, open("{}/{}.json".format(MOVIE_DIR, str(credit['id'])), "w"))


create_dir(MOVIE_DIR)

actor_name = "Tom Holland"
actor_id = get_actor_id(actor_name)

actor_credits = get_actor_credits(actor_id)

# print(actor_credits)
