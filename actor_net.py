import urllib
import urllib.request
import urllib.parse
from unidecode import unidecode

import json

import config

TMDB_ACTOR_URL = "https://api.themoviedb.org/3/search/person?api_key=%s&language=en-US&query=%s&page=1"
TMDB_CREDITS_URL = "https://api.themoviedb.org/3/person/%s/combined_credits?api_key=%s&language=en-US"

tmdb_api_key = config.tmdb_api_key

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

    return jres['cast']

actor_name = "Tom Holland"
actor_id = get_actor_id(actor_name)

actor_credits = get_actor_credits(actor_id)

print(actor_credits)