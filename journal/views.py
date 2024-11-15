from django.core.files.base import File, ContentFile
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.apps import apps
from datetime import datetime
from io import StringIO

import json
from . import tmdb
from .models import Viewing, Film, ImportedFile, Follow


# Create your views here.

def index(request, user=None):
    """
    Basic page showing journal for logged-in user or another user if specified.

    :param user: str
        username of the user whose journal to display
    """
    viewings = []
    username = ""
    displayname = ""
    private = False
    follows = False
    following = []

    if request.user.is_authenticated:
        following = [f.followed.username
                     for f in request.user.following.all()]

    if user is not None:
        # check for existence of user
        JUser = apps.get_model('accounts', 'JUser')
        matches = JUser.objects.filter(username=user)
        if matches.exists():
            user_obj = matches[0]
            username = user_obj.username
            # check if following this user
            if request.user.is_authenticated:
                if Follow.objects.filter(follower=request.user,
                                         followed=user_obj).exists():
                    follows = True
            displayname = user_obj.displayname
            if username != request.user.username and user_obj.private:
                viewings = []
                private = True
            else:
                viewings = user_obj.viewings.all().order_by("-date")
        else:
            username = "__no_such_user__"

    elif request.user.is_authenticated:
        # use logged-in user
        viewings = request.user.viewings.all().order_by("-date")
        username = request.user.username
        displayname = request.user.displayname

    return render(request, "journal/index.html",
                  {
                      "username": username,
                      "displayname": displayname,
                      "viewings": viewings,
                      "private": private,
                      "follows": follows,
                      "following": following,
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
    viewing_json = {}
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
                               .get("title", "unknown")),
                        original_title=(request.session
                                        .get("candidates", {})
                                        .get(tmdb_id, {})
                                        .get("original_title", "unknown")),
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
        viewing_json = {"id": viewing.pk,
                        "title": viewing.film.title,
                        "cinema_or_tv": viewing.cinema_or_tv,
                        "comments": viewing.comments}
    return JsonResponse({
        "response": "I think I did what you wanted (save)",
        "viewing": viewing_json,
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
                "comments": viewing.comments,
                "private": viewing.private
            }
            return JsonResponse(viewing_dict)
        except Viewing.DoesNotExist:
            return JsonResponse({
                "error": "viewing_id not found in database"
            })


def follow(request):
    """
    Create or delete a follow relationship between two users
    """
    JUser = apps.get_model('accounts', 'JUser')
    if request.method == "POST":
        instructions = json.loads(request.body)
        follower = instructions.get("follower", "")
        if follower != request.user.username:
            return JsonResponse({"error": "follower not active user"})
        followed = instructions.get("followed", "")
        # find followed user id
        try:
            followed_user_obj = JUser.objects.get(username=followed)
        except JUser.DoesNotExist as e:
            return JsonResponse({"error": "followed user does not exist"})

        action = instructions.get("action")
        if action == "follow":
            follow_obj = Follow(follower=request.user,
                                followed=followed_user_obj)
            follow_obj.save()
            return JsonResponse({"result": "now following!"})
        else:
            # find the follow object and delete it
            follow_objs = Follow.objects.filter(follower=request.user,
                                                followed=followed_user_obj)
            print(follow_objs)
            for follow_obj in follow_objs:
                follow_obj.delete()

            return JsonResponse({"result": "no longer following!"})


def import_tool(request):
    """
    Basic view for the data import tool.  Accepts file upload -- must be
    json list of dicts with keys corresponding to columns in Film and Viewing
    tables (but can have other keys that are ignored)
    """
    uploaded_files = [uf.name for uf
                      in ImportedFile.objects.filter(user=request.user)]
    if request.method == "POST":
        content_type = request.META.get("CONTENT_TYPE")
        # implement DELETE viewings file
        if content_type == "application/json":
            json_request = json.loads(request.body)
            request_action = json_request.get("action", None)
            if request_action == "delete_viewings_file":
                filename = request.session["uploaded_file"]
                print(f"going to delete {filename}!")
                file_obj = ImportedFile.objects.get(user=request.user,
                                                    name=filename)
                file_obj.delete()
                # clear file data from request.session
                del request.session["file_loaded"]
                del request.session["uploaded_file"]
                del request.session["uploaded_viewings"]

            elif request_action == "close_viewings_file":
                del request.session["file_loaded"]
                del request.session["uploaded_file"]
                del request.session["uploaded_viewings"]

            elif "validated" in json_request:
                # it must be an update to a viewing in the import list

                viewing_number = json_request["validated"]
                request.session["uploaded_viewings"][viewing_number]["validated"] = True
                request.session.modified = True
                # write updated viewings to file
                print("updating file on disk!")
                with (ImportedFile
                        .objects
                        .get(pk=request.session["file_loaded"])
                        .upload
                        .open("w")) as jsf:
                    json.dump(
                        [viewing for k, viewing
                         in request.session["uploaded_viewings"].items()],
                        jsf, indent=2, sort_keys=True
                    )

            # render the updated import page
            return redirect("import_tool")

        else:
            # check if the POST request contains a viewings_file:
            if "viewings_file" in request.FILES:

                # process uploaded file
                viewings_file = request.FILES.get("viewings_file")

                # if filename doesn't already exist, process it!
                # TODO: tell user if file already exists!
                if viewings_file.name not in uploaded_files:

                    viewings = json.load(viewings_file)
                    # replace ampersand characters:
                    for viewing in viewings:
                        viewing["title"] = viewing["title"].replace("&", "and")
                        # if no "validated" field, add it:
                        if "validated" not in viewing:
                            viewing["validated"] = False

                    # automatically process all viewings with "tmdb" field and valid date
                    for viewing in viewings:
                        processed_viewing = tmdb.validate_viewing(viewing)
                        # print(processed_viewing)
                        if "error" in processed_viewing:
                            print(viewing["title"])
                            print(processed_viewing["error"])
                            continue

                        # save Film and Viewing to databases
                        film_dict = processed_viewing["film_dict"]
                        viewing_dict = processed_viewing["viewing_dict"]

                        # check if Film already in database
                        filmobjs = Film.objects.filter(tmdb=film_dict["tmdb"])
                        if len(filmobjs) > 0:
                            filmobj = filmobjs[0]
                            # print(f"found film: {film_dict['title']}")
                        else:
                            filmobj = Film(
                                tmdb=film_dict["tmdb"],
                                title=film_dict["title"],
                                original_title=film_dict["original_title"],
                                release_date=film_dict["release_date"],
                                year=film_dict["year"],
                                director=film_dict["director"],
                                starring=", ".join(film_dict["starring"]),
                                overview=film_dict["overview"]
                            )
                            filmobj.save()
                            # print(f"saved film: {film_dict['title']}")

                        # check if Viewing object is already in database
                        if (Viewing.objects.filter(
                                user=request.user,
                                film=filmobj,
                                date=viewing_dict["date"]).exists()):
                            # print(f"viewing of {film_dict['title']} exists")
                            pass
                        else:
                            viewingobj = Viewing(
                                user=request.user,
                                film=filmobj,
                                date=viewing_dict["date"],
                                location=viewing_dict["location"],
                                cinema_or_tv=viewing_dict["cinema_or_tv"],
                                tv_channel=viewing_dict["tv_channel"],
                                streaming_platform=viewing_dict["streaming_platform"],
                                cinema=viewing_dict["cinema"],
                                private=viewing_dict["private"],
                                comments=viewing_dict["comments"]
                            )
                            viewingobj.save()
                            # print("saved viewing!")

                        viewing["validated"] = True

                    # store the uploaded file in the database
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

                    # set loaded_file in request.session
                    IFobj = ImportedFile.objects.get(user=request.user,
                                                     name=viewings_file.name)
                    request.session["file_loaded"] = IFobj.pk

                    # cache the uploaded viewings
                    request.session["uploaded_viewings"] = {
                        (ii + 1): viewing
                        for ii, viewing in enumerate(viewings)
                    }
                    request.session["uploaded_file"] = viewings_file.name
                    uploaded_file = viewings_file.name

                else:
                    viewings = []
                    uploaded_file = ""
                return render(request, "journal/import.html",
                              {
                                  "username": request.user.username,
                                  "displayname": request.user.displayname,
                                  "viewings": viewings,
                                  "uploaded_files": uploaded_files,
                                  "uploaded_file": (uploaded_file
                                                    .rsplit(".",
                                                            1)[0])
                              })

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
                    request.session["uploaded_file"] = filename

    if "uploaded_viewings" in request.session:
        viewings = [viewing for k, viewing
                    in request.session["uploaded_viewings"].items()]
        uploaded_file = request.session["uploaded_file"]
    else:
        viewings = []
        uploaded_file = ""

    return render(request, "journal/import.html",
                  {
                      "username": request.user.username,
                      "displayname": request.user.displayname,
                      "viewings": viewings,
                      "uploaded_files": uploaded_files,
                      "uploaded_file": uploaded_file.rsplit(".", 1)[0]
                  })


def export_data(request):
    # get query-set of user's viewings
    viewings = list(Viewing.objects.filter(user__id=request.user.id).values())
    # add film info for each viewing
    for viewing in viewings:
        # don't need to export user_id and film_id
        viewing.pop("user_id")
        film_id = viewing.pop("film_id")
        # convert date to string
        viewing["date"] = datetime.strftime(viewing["date"],
                                            "%Y-%m-%d")
        # get film info and add it to viewing for export
        film_data = Film.objects.get(id=film_id)
        print(film_data.title)
        viewing["tmdb"] = film_data.tmdb
        viewing["title"] = film_data.title
        viewing["year"] = film_data.year
        viewing["original_title"] = film_data.original_title
        viewing["director"] = film_data.director
        viewing["starring"] = film_data.starring
        viewing["release_date"] = datetime.strftime(film_data.release_date,
                                                    "%Y-%m-%d")
    # prepare response
    content = ContentFile(json.dumps(viewings,
                                     indent=2,
                                     sort_keys=False).encode("latin-1"),
                          name="cinefile_export.json")
    content.in_memory = False
    response = HttpResponse(content, content_type="application/json")
    response["Content-Disposition"] = \
        'attachment; filename="cinefile_export.json"'
    return response


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


def find_users(request):
    """
    find public cinefiles by username pattern
    """
    matching_users = []
    if request.method == "GET":
        search_string = request.GET.get("username", None)
        JUser = apps.get_model('accounts', 'JUser')

        if search_string is not None:
            users = JUser.objects.filter(username__icontains=search_string)
            matching_users = [u.username for u in users if not u.private]
    return JsonResponse({
        "matching_users": matching_users
    })


# mobile views
def mobile_index(request, user=None):
    """
    Mobile-friendly page showing journal for logged-in user or another user
    if specified.
    """
    viewings = []
    username = ""
    displayname = ""
    private = False
    follows = False
    following = []

    if request.user.is_authenticated:
        following = [f.followed.username
                     for f in request.user.following.all()]

    if user is not None:
        # check for existence of user
        JUser = apps.get_model('accounts', 'JUser')
        matches = JUser.objects.filter(username=user)
        if matches.exists():
            user_obj = matches[0]
            username = user_obj.username
            # check if following this user
            if request.user.is_authenticated:
                if Follow.objects.filter(follower=request.user,
                                         followed=user_obj).exists():
                    follows = True
            displayname = user_obj.displayname
            if username != request.user.username and user_obj.private:
                viewings = []
                private = True
            else:
                viewings = user_obj.viewings.all().order_by("-date")
        else:
            username = "__no_such_user__"

    elif request.user.is_authenticated:
        # use logged-in user
        viewings = request.user.viewings.all().order_by("-date")
        username = request.user.username
        displayname = request.user.displayname

    return render(request, "journal/mobile_index.html",
                  {
                      "username": username,
                      "displayname": displayname,
                      "viewings": viewings,
                      "private": private,
                      "follows": follows,
                      "following": following,
                  })

