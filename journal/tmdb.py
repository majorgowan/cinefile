import requests
import json
from django.conf import settings


base_url = f"https://api.themoviedb.org/3"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_AUTH}"
}


def search_movie(pattern, **kwargs):
    """
    Search TMDB by title

    :param pattern: str
        search pattern
    :param kwargs: dict
        get parameters
    :return: dict
    """
    page = kwargs.get("page", 1)
    url_end = f"search/movie?query={pattern}&page={page}"
    url_full = f"{base_url}/{url_end}"
    response = requests.get(url_full, headers=headers)
    if response.status_code == 200:
        rj = json.loads(response.text)
        # strip punctuation from query
        search_results = {
            "status_code": response.status_code,
            "candidates": {
                res["id"]: {
                    "title": res["title"],
                    "original_title": res["original_title"],
                    "release_date": res["release_date"],
                    "year": res["release_date"][:4],
                    "overview": res["overview"]
                } for res in rj["results"]
            },
            "page": rj["page"],
            "total_pages": rj["total_pages"]
        }
        return search_results
    else:
        return {
            "error": response.text,
            "status_code": response.status_code
        }


def movie_credits(imdb_id, nstars=5):
    """
    Retrieve movie credits from TMDB

    :param imdb_id: str
        search pattern
    :param nstars: int
        number of stars to return
    :return: dict
    """
    url_end = f"movie/{imdb_id}/credits"
    url_full = f"{base_url}/{url_end}"
    response = requests.get(url_full, headers=headers)
    if response.status_code == 200:
        rj = json.loads(response.text)
        directors = [person["name"] for person in rj["crew"]
                     if person.get("job", "").lower() == "director"]
        if len(directors) == 0:
            director = "unknown"
        else:
            director = directors[0]
        stars = [person["name"] for person in rj["cast"]]
        return {
            "status_code": response.status_code,
            "imdb_id": imdb_id,
            "director": director,
            "starring": stars[:nstars]
        }
    else:
        return {
            "error": response.text,
            "status_code": response.status_code
        }
