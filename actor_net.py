import urllib
import urllib.request
import urllib.parse
from unidecode import unidecode
from tqdm import tqdm

import json
import os

import config

TMDB_ACTOR_URL = "https://api.themoviedb.org/3/search/person?api_key=%s&language=en-US&query=%s&page=1"
TMDB_ACTOR_CREDITS_URL = "https://api.themoviedb.org/3/person/%s/combined_credits?api_key=%s&language=en-US"
TMDB_MOVIE_CREDITS_URL = "https://api.themoviedb.org/3/movie/%s/credits?api_key=%s&language=en-US"

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

    url = TMDB_ACTOR_CREDITS_URL % (urllib.parse.quote(str(actor_id)), tmdb_api_key)
    response = urllib.request.urlopen(url)
    res_data = response.read()
    jres = json.loads(res_data)

    credits = jres['cast']
    credit_ids = []

    for credit in credits:
        json.dump(credit, open("{}/{}.json".format(MOVIE_DIR, str(credit['id'])), "w"))
        credit_ids.append(str(credit['id']))
    
    with open('{}/{}.txt'.format(DATA_DIR, actor_name), 'w', encoding='utf-8') as f:
        f.write(str.join('\n', (str(x) for x in credit_ids)))

def get_ego_center_credits(actor_name):
    # create the users friend list
    credit_ids = []
    try:
        with open('{}/{}.txt'.format(DATA_DIR, actor_name)) as f:
            for line in f:
                credit_ids.append(int(line))
    except Exception as e:
        print("Error: ", e)
        pass
    return (credit_ids)

def get_movie_actors(credit_ids):
    for credit in tqdm(credit_ids):
        if is_folder_exists('{}/{}.json'.format(MOVIE_DIR, str(credit))):
            saved = json.load(open("{}/{}.json".format(MOVIE_DIR, str(credit)), "r"))
            if saved['media_type'] == 'movie':
                try:
                    url = TMDB_MOVIE_CREDITS_URL % (credit, tmdb_api_key)
                    response = urllib.request.urlopen(url)
                    res_data = response.read()
                    jres = json.loads(res_data)

                    actors = jres['cast']
                    actor_ids = []

                    for actor in actors:
                        actor_ids.append(str(actor['id']))
                    
                    with open('{}/{}.txt'.format(ACTOR_DIR, str(actor['id'])), 'w', encoding='utf-8') as f:
                        f.write(str.join('\n', (str(x) for x in actor_ids)))
                except Exception as e:
                    print("Error collecting ", credit)



actor_name = "Tom Holland"
DATA_DIR = "data"
MOVIE_DIR = "{}/{}".format(DATA_DIR, "movies")
ACTOR_DIR = "{}/{}".format(DATA_DIR, actor_name)

create_dir(MOVIE_DIR)
create_dir(ACTOR_DIR)

# actor_id = get_actor_id(actor_name)

# get_actor_credits(actor_id)

credit_ids = get_ego_center_credits(actor_name)

get_movie_actors(credit_ids)

# print(actor_credits)
