import urllib
import urllib.request
import urllib.parse
from unidecode import unidecode
from tqdm import tqdm
import networkx as nx

import json
import os
from itertools import combinations

import config

TMDB_ACTOR_URL = "https://api.themoviedb.org/3/search/person?api_key=%s&language=en-US&query=%s&page=1"
TMDB_ACTOR_CREDITS_URL = "https://api.themoviedb.org/3/person/%s?api_key=%s&language=en-US&append_to_response=combined_credits"
TMDB_MOVIE_CREDITS_URL = "https://api.themoviedb.org/3/movie/%s/credits?api_key=%s&language=en-US"
TMDB_TV_CREDITS_URL = "https://api.themoviedb.org/3/tv/%s/credits?api_key=%s&language=en-US"

tmdb_api_key = config.tmdb_api_key
actor_name = config.actor_name


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

    url = TMDB_ACTOR_CREDITS_URL % (
        urllib.parse.quote(str(actor_id)), tmdb_api_key)
    response = urllib.request.urlopen(url)
    res_data = response.read()
    jres = json.loads(res_data)

    credits = jres['combined_credits']['cast']
    credit_ids = []

    for credit in credits:
        json.dump(credit, open(
            "{}/{}.json".format(MOVIE_DIR, str(credit['id'])), "w"))
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
    all_actors = []
    for credit in tqdm(credit_ids):
        if is_folder_exists('{}/{}.json'.format(MOVIE_DIR, str(credit))):
            saved = json.load(
                open("{}/{}.json".format(MOVIE_DIR, str(credit)), "r"))
            if saved['media_type'] == 'movie':
                url = TMDB_MOVIE_CREDITS_URL % (credit, tmdb_api_key)
            elif saved['media_type'] == 'tv':
                url = TMDB_TV_CREDITS_URL % (credit, tmdb_api_key)
            try:
                response = urllib.request.urlopen(url)
                res_data = response.read()
                jres = json.loads(res_data)

                actors = jres['cast']
                actor_ids = []

                for actor in actors:
                    if actor['known_for_department'] == "Acting":
                        actor_ids.append(str(actor['id']))
                all_actors += actor_ids

                # with open('{}/{}.txt'.format(ACTOR_DIR, str(actor['id'])), 'w', encoding='utf-8') as f:
                #     f.write(str.join('\n', (str(x) for x in actor_ids)))
            except Exception as e:
                print("Error collecting ", credit)

    with open('{}/{}.txt'.format(DATA_DIR, "actor_ids"), 'w', encoding='utf-8') as f:
        f.write(str.join('\n', (str(x) for x in list(set(all_actors)))))


def get_actor_ids():
    actor_ids = []
    try:
        with open('{}/{}.txt'.format(DATA_DIR, "actor_ids")) as f:
            for line in f:
                actor_ids.append(int(line))
    except Exception as e:
        print("Error: ", e)
        pass
    return actor_ids


def get_second_order_credits(actor_ids):
    actor_details = {}
    for actor_id in tqdm(actor_ids):
        try:
            url = TMDB_ACTOR_CREDITS_URL % (
                urllib.parse.quote(str(actor_id)), tmdb_api_key)
            response = urllib.request.urlopen(url)
            res_data = response.read()
            jres = json.loads(res_data)

            credits = jres['combined_credits']['cast']
            credit_ids = []

            for credit in credits:
                credit_ids.append(str(credit['id']))

            with open('{}/{}.txt'.format(ACTORS_DIR, actor_id), 'w', encoding='utf-8') as f:
                f.write(str.join('\n', (str(x) for x in credit_ids)))

            details = {
                "name": jres["name"],
                "gender": jres["gender"],
                "birthday": jres["birthday"],
                "deathday": jres["deathday"],
                "tmdb_id": jres["id"],
                "imdb_id": jres["imdb_id"],
                "place_of_birth": jres["place_of_birth"],
                "popularity": jres["popularity"],
            }
            actor_details[str(actor_id)] = details

        except Exception as e:
            print("Error: ", e)

    json.dump(actor_details, open(
        "{}/{}.json".format(DATA_DIR, "actor_details"), "w"))


def get_ego_center_details(actor_name):
    actor_id = get_actor_id(actor_name)
    url = TMDB_ACTOR_CREDITS_URL % (
        urllib.parse.quote(str(actor_id)), tmdb_api_key)
    response = urllib.request.urlopen(url)
    res_data = response.read()
    jres = json.loads(res_data)

    details = {
        "name": jres["name"],
        "gender": jres["gender"],
        "birthday": jres["birthday"],
        "deathday": jres["deathday"],
        "tmdb_id": jres["id"],
        "imdb_id": jres["imdb_id"],
        "place_of_birth": jres["place_of_birth"],
        "popularity": jres["popularity"],
    }

    json.dump(details, open(
        "{}/{}.json".format(DATA_DIR, actor_name), "w"))


def get_credits(actor_id):
    # create the users friend list
    credits = []
    try:
        with open('{}/{}.txt'.format(ACTORS_DIR, actor_id)) as f:
            for line in f:
                credits.append(int(line))
    except Exception as e:
        print("Error: ", e)
        pass
    return (credits)


def generate_graph(actor_name):

    actor_details = json.load(open("{}/{}.json".format(DATA_DIR, "actor_details"), "r"))
    ego_details = json.load(open("{}/{}.json".format(DATA_DIR, actor_name), "r"))
    ego_details = {key: ego_details[key] if ego_details[key]!=None else "" for key in ego_details}
    actor_ids = list(actor_details.keys())

    pairs = list(combinations(actor_ids, 2))

    G = nx.Graph()
    
    ego_credits = []
    with open('{}/{}.txt'.format(DATA_DIR, actor_name)) as f:
        for line in f:
            ego_credits.append(int(line))

    ego_details['common'] = len(ego_credits)

    for actor in actor_details:
        alter_credits = set(get_credits(actor))
        common = list(alter_credits.intersection(set(ego_credits)))
        details = actor_details[actor]
        details = {key: details[key] if details[key]!=None else "" for key in details}
        details['common'] = len(common)

        G.add_nodes_from([(details['name'], details)])

    G.add_nodes_from([(ego_details['name'], ego_details)])

    for a, b in tqdm(pairs):
        a_credits = set(get_credits(a))
        b_credits = set(get_credits(b))

        common = list(a_credits.intersection(b_credits))
        if len(common) > 0:
            G.add_edge(actor_details[a]['name'], actor_details[b]['name'], weight=len(common))
    
    for alter in tqdm(actor_ids):
        alter_credits = set(get_credits(alter))
        common = list(alter_credits.intersection(set(ego_credits)))
        if len(common) > 0:
            G.add_edge(ego_details['name'], actor_details[alter]['name'], weight=len(common))

    G.remove_edges_from(nx.selfloop_edges(G))
    nx.write_gml(G, "{}/{}.gml".format(DATA_DIR, actor_name))



DATA_DIR = "data"
MOVIE_DIR = "{}/{}".format(DATA_DIR, "movies")
ACTOR_DIR = "{}/{}".format(DATA_DIR, actor_name)
ACTORS_DIR = "{}/{}".format(DATA_DIR, "actors")

create_dir(MOVIE_DIR)
create_dir(ACTOR_DIR)
create_dir(ACTORS_DIR)

print("Get movies acted in")
actor_id = get_actor_id(actor_name)
get_actor_credits(actor_id)

print("Get actors from movies")
credit_ids = get_ego_center_credits(actor_name)
get_movie_actors(credit_ids)

print("Get second order movie credits")
actor_ids = get_actor_ids()
get_second_order_credits(actor_ids)

get_ego_center_details(actor_name)

print("Generating graph")
generate_graph(actor_name)

# print(actor_credits)
