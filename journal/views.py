from django.core.files.base import File
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.apps import apps
from datetime import datetime
from io import StringIO

import json
from . import tmdb
from .models import Viewing, Film, ImportedFile


# Create your views here.
def index(request, user=None):
    """
    Basic page showing journal for logged-in user or another user if specified.

    :param user: str
        username of the user whose journal to display
    """
    viewings = []
    username = ""
    if user is not None:
        # check for existence of user
        JUser = apps.get_model('accounts', 'JUser')
        matches = JUser.objects.filter(username=user)
        if len(matches) == 1:
            user_obj = matches[0]
            username = user_obj.username
            viewings = user_obj.viewings.all().order_by("-date")
    elif request.user.is_authenticated:
        # use logged-in user
        viewings = request.user.viewings.all().order_by("-date")
        username = request.user.username
    return render(request, "journal/index.html",
                  {
                      "username": username,
                      "viewings": viewings,
                  })


def tmdb_search(request, api_command):
    """
    Query the TMDB database either to _search_ for a film by title or
    to retrieve the credits information for a film with known TMDB (IAFD) id.

    :param api_command: str
        one of "search" and "credits"
    """
    if "searches" not in request.session:
        request.session["searches"] = {}
    if "credits" not in request.session:
        request.session["credits"] = {}
    if request.method == "GET":
        # call TMDB API
        if api_command == "search":
            query = request.GET.get("pattern", "")
            page = int(request.GET.get("page", 1))
            cache_key = f"{query}---{page}"
            if cache_key in request.session["searches"]:
                result = request.session["searches"][cache_key]
                candidates = result["candidates"]
            else:
                search_results = tmdb.search_movie(query, page=page)
                if search_results["status_code"] != 200:
                    print(search_results)
                    return JsonResponse({},
                                        status=search_results["status_code"])
                candidates = search_results["candidates"]
                total_pages = search_results["total_pages"]
                result = {
                    "query": query,
                    "candidates": candidates,
                    "page": page,
                    "last_page": False,
                    "total_pages": total_pages
                }
                # cache search in session:
                request.session["searches"][cache_key] = result
            # cache candidates in session object as last search
            request.session["candidates"] = candidates
            return JsonResponse(result)

        elif api_command == "credits":
            movie_id = request.GET.get("movie_id", "")
            if movie_id in request.session["credits"]:
                details = request.session["credits"][movie_id]
            else:
                details = tmdb.movie_credits(movie_id, nstars=5)
                if details["status_code"] != 200:
                    print(details)
                    return JsonResponse({},
                                        status=details["status_code"])
                # cache search result
                request.session["credits"][movie_id] = details
            # cache movie details as latest result
            request.session["tmdb"] = movie_id
            request.session["director"] = details["director"]
            request.session["starring"] = details["starring"]
            return JsonResponse(details)
        else:
            return JsonResponse({"error": f"{api_command} not implemented"})


def new_viewing(request):
    """
    Register a new Viewing instance (and a new Film instance if the film
    is not already in the database)
    """
    if request.method == "POST":
        form = request.POST

        # check if this is a new viewing or an update
        viewing_update_hidden = form.get("viewing_update_hidden", "")
        pk = None
        if viewing_update_hidden != "new":
            try:
                pk = int(viewing_update_hidden)
            except Exception as e:
                print(e)

        if pk is not None:
            # get tmdb_id from the database
            tmdb_id = Viewing.objects.get(id=pk).film.tmdb
        else:
            # get tmdb_id from session variable (last searched)
            tmdb_id = request.session.get("tmdb", None)

        # populate and save new Film entry
        # (first check if tmdb_id is already in Films table)
        if Film.objects.filter(tmdb=tmdb_id).exists():
            film = Film.objects.get(tmdb=tmdb_id)
        else:
            film = Film(tmdb=int(request.session.get("tmdb", 0)),
                        title=(request.session
                               .get("candidates", {})
                               .get(tmdb_id, {})
                               .get("title", "unkown")),
                        original_title=(request.session
                                        .get("candidates", {})
                                        .get(tmdb_id, {})
                                        .get("original_title", "unkown")),
                        release_date=(request.session
                                      .get("candidates", {})
                                      .get(tmdb_id, {})
                                      .get("release_date", None)),
                        year=(request.session
                              .get("candidates", {})
                              .get(tmdb_id, {})
                              .get("year", None)),
                        director=request.session.get("director", None),
                        starring=", ".join(request.session.get("starring")),
                        overview=(request.session
                                  .get("candidates", {})
                                  .get(tmdb_id, {})
                                  .get("overview", None)))
            film.save()
        # populate and save new Viewing entry
        private_checkbox = form.get("private", "off")
        viewing = Viewing(pk=pk,
                          user=request.user,
                          film=film,
                          date=form.get("date"),
                          location=form.get("location"),
                          cinema_or_tv=form.get("cinema_video_select"),
                          tv_channel=form.get("channel"),
                          streaming_platform=form.get("platform"),
                          cinema=form.get("cinema"),
                          private=(private_checkbox == "on"),
                          comments=form.get("comments"))
        viewing.save()
    return JsonResponse({
        "response": "I think I did what you wanted (save)"
    })


def delete_viewing(request):
    """
    Delete an existing viewing
    """
    if request.method == "POST":
        post_request = json.loads(request.body)
        # print(post_request)
        # delete the viewing from the database
        pk = int(post_request["viewing_id"])
        to_delete = Viewing.objects.get(pk=pk)
        # print(to_delete)
        to_delete.delete()
    return JsonResponse({
        "response": "I think I did what you wanted (delete)"
    })


def query_viewing(request):
    """
    Retrieve a Viewing instance from the database (for editing purposes)
    """
    if request.method == "GET":
        viewing_id = request.GET.get("viewing_id", "")
        try:
            viewing = Viewing.objects.get(id=viewing_id)
            viewing_dict = {
                "film_id": viewing.film.id,
                "film_title": viewing.film.title,
                "date": datetime.strftime(viewing.date, format="%Y-%m-%d"),
                "location": viewing.location,
                "cinema_or_tv": viewing.cinema_or_tv,
                "video_medium": viewing.video_medium,
                "tv_channel": viewing.tv_channel,
                "streaming_platform": viewing.streaming_platform,
                "cinema": viewing.cinema,
                "comments": viewing.comments
            }
            return JsonResponse(viewing_dict)
        except Viewing.DoesNotExist:
            return JsonResponse({
                "error": "viewing_id not found in database"
            })


def import_tool(request):
    """
    Basic view for the data import tool.  Accepts file upload -- must be
    json list of dicts with keys corresponding to columns in Film and Viewing
    tables (but can have other keys that are ignored)
    """
    uploaded_files = [uf.name for uf
                      in ImportedFile.objects.filter(user=request.user)]
    if request.method == "POST":
        # check if the POST request contains a viewings_file:
        if "viewings_file" in request.FILES:
            # process uploaded file
            viewings_file = request.FILES.get("viewings_file")
            if viewings_file is not None:
                viewings = json.load(viewings_file)
                # replace ampersand characters:
                for viewing in viewings:
                    viewing["title"] = viewing["title"].replace("&", "and")
                    # if no "validated" field, add it:
                    if "validated" not in viewing:
                        viewing["validated"] = False
                if viewings_file not in uploaded_files:
                    # if it's new, store the processed file
                    print("Going to save the file now!!!")
                    importedFile = ImportedFile(
                        user=request.user,
                        name=viewings_file.name,
                        upload=File(name=viewings_file.name,
                                    file=StringIO(json.dumps(viewings,
                                                             sort_keys=True,
                                                             indent=2)))
                    )
                    importedFile.save()
                    # update the list of uploaded_files
                    uploaded_files = [uf.name for uf
                                      in (ImportedFile.objects
                                          .filter(user=request.user))]
                # cache the uploaded viewings
                request.session["uploaded_viewings"] = {
                    (ii + 1): viewing
                    for ii, viewing in enumerate(viewings)
                }
            else:
                viewings = []
            return render(request, "journal/import.html",
                          {
                              "username": request.user.username,
                              "viewings": viewings,
                              "uploaded_files": uploaded_files
                          })
        else:
            # process POST request with processed viewing
            post_request = json.loads(request.body)
            if "validated" in post_request:
                viewing_number = post_request["validated"]
                request.session["uploaded_viewings"][viewing_number]["validated"] = True
                request.session.modified = True
                # write updated viewings to file
                with (ImportedFile
                      .objects
                      .get(pk=request.session["file_loaded"])
                      .upload
                      .open("w")) as jsf:
                    json.dump([viewing for k, viewing
                               in request.session["uploaded_viewings"].items()],
                              jsf, indent=2, sort_keys=True)
            # render the import page with the updated validated flag
            return redirect("import_tool")

    elif request.method == "GET":
        # get request to load previously imported file
        filename = request.GET.get("filename", "")
        if "file_loaded" in request.session:
            filename_loaded = (ImportedFile
                               .objects
                               .get(pk=request.session["file_loaded"])).name
        else:
            filename_loaded = ""
        if filename != filename_loaded:
            if (ImportedFile.objects.filter(name=filename,
                                            user=request.user).exists()):
                IFobj = ImportedFile.objects.get(name=filename)
                if IFobj.pk != request.session.get("file_loaded", None):
                    viewings = json.load(IFobj.upload)
                    request.session["uploaded_viewings"] = {
                        (ii + 1): viewing
                        for ii, viewing in enumerate(viewings)
                    }
                    request.session["file_loaded"] = IFobj.pk
    if "uploaded_viewings" in request.session:
        viewings = [viewing for k, viewing
                    in request.session["uploaded_viewings"].items()]
    else:
        viewings = []
    return render(request, "journal/import.html",
                  {
                      "username": request.user.username,
                      "viewings": viewings,
                      "uploaded_files": uploaded_files
                  })


def get_session_data(request):
    """
    Utility view to make uploaded file content (or anything else in session
    object) available to a json script.
    """
    if request.method == "GET":
        key = request.GET.get("key", "")
        subkey = request.GET.get("subkey", "0")
        if key in request.session:
            if subkey in request.session[key]:
                return JsonResponse(
                    request.session[key][subkey]
                )
            else:
                return JsonResponse({
                    key: request.session[key]
                })
        else:
            return JsonResponse({
                "error": f"{key} is not in session"
            })
