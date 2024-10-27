import requests
import json
from django.conf import settings
from datetime import datetime

from .models import Film

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
                    "original_language": res.get("original_language", ""),
                    "release_date": res.get("release_date", ""),
                    "year": res.get("release_date", "")[:4],
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


def movie_details(tmdb_id):
    """
    Retrieve movie details from TMDB, i.e.
        title
        original_title
        original_language
        release_date
        runtime
        year
        overview

    :param tmdb_id: str
        TMDB id of film for which to retrieve details
    :return: dict
    """
    url_end = f"movie/{tmdb_id}"
    url_full = f"{base_url}/{url_end}"
    response = requests.get(url_full, headers=headers)
    if response.status_code == 200:
        rj = json.loads(response.text)
        return {
            "status_code": response.status_code,
            "tmdb_id": rj["id"],
            "year": rj["release_date"][:4],
            "title": rj["title"],
            "original_title": rj.get("original_title", rj["title"]),
            "original_language": rj.get("original_language", ""),
            "runtime": rj.get("runtime", None),
            "release_date": rj["release_date"],
            "overview": rj.get("overview", "")
        }
    else:
        return {
            "error": response.text,
            "status_code": response.status_code
        }


def movie_credits(tmdb_id, nstars=5):
    """
    Retrieve movie credits from TMDB

    :param tmdb_id: str
        TMDB id of film for which to retrieve credits
    :param nstars: int
        number of stars to return
    :return: dict
    """
    url_end = f"movie/{tmdb_id}/credits"
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
            "tmdb_id": tmdb_id,
            "director": director,
            "starring": stars[:nstars]
        }
    else:
        return {
            "error": response.text,
            "status_code": response.status_code
        }


def validate_viewing(viewing):
    """
    Provided viewing info including "tmdb" field with the TMDB id and
    a valid date string, query local database and then TMDB if
    necessary.

    :param viewing:
    :return: dict
        if valid, return dict with "Film" and "Viewing" keys and objects
        for adding to databases; if invalid, provide list of errors
        ("invalid date", "missing tmdb", ...)
    """
    viewing_dict = {}

    if "date" not in viewing:
        return {"error": "missing date"}

    try:
        viewing_dict["date"] = datetime.strptime(viewing["date"],
                                                 "%Y-%m-%d")
    except ValueError as ve:
        return {"error": f"invalid date -- {ve}"}

    if "tmdb" not in viewing:
        return {"error": "missing tmdb"}

    filmobjs = Film.objects.filter(tmdb=viewing["tmdb"])
    if filmobjs.exists():
        # already in the database, don't trouble TMDB!
        film_dict = {"tmdb": filmobjs[0].tmdb}
    else:
        # query tmdb for film info
        credits = movie_credits(viewing["tmdb"])
        if credits["status_code"] != 200:
            return {"error": f"tmdb credits error -- {credits['error']}"}
        details = movie_details(viewing["tmdb"])
        if details["status_code"] != 200:
            return {"error": f"tmdb details error -- {details['error']}"}

        film_dict = {
            "tmdb": credits["tmdb_id"],
            "starring": credits["starring"],
            "director": credits["director"],
            "release_date": details["release_date"],
            "year": details["year"],
            "title": details["title"],
            "original_title": details["original_title"],
            "overview": details["overview"]
        }

    viewing_dict.update({
        "comments": viewing.get("comments", ""),
        "location": viewing.get("location", ""),
        "cinema_or_tv": viewing.get("cinema_or_tv", ""),
        "tv_channel": viewing.get("tv_channel", ""),
        "streaming_platform": viewing.get("streaming_platform", ""),
        "cinema": viewing.get("cinema", ""),
        "private": viewing.get("private", False)
    })

    return {"film_dict": film_dict,
            "viewing_dict": viewing_dict}