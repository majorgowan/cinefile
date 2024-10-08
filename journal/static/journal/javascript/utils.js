// script for parsing browser cookie
function get_cookie(cookie_name) {
    const cookie_value = (document
                          .cookie.split("; ")
                          .find(row => row.startsWith(`${cookie_name}=`))?.split('=')[1]);
    return cookie_value;
}

function replaceElement(element) {
    const new_element = element.cloneNode(true);
    element.parentNode.replaceChild(new_element, element);
    // console.log(new_element);
    return new_element;
}

function process_tmdb_search(searchData) {

    let innercontent = "<ul>";
    const page = searchData["page"];
    const total_pages = searchData["total_pages"];

    for (const key in searchData.candidates) {
        year = searchData.candidates[key]["year"];
        title = searchData.candidates[key]["title"];
        innercontent = innercontent + `<li><a class="movie_search_link", data-movie_id="${key}">${title} (${year})</a></li>`;
    }
    innercontent = innercontent + "</ul>"

    let footer = "";
    // if page greater than 1, add link to previous page
    if (page > 1) {
        const prev_page = "" + (parseInt(page) - 1);
        footer = footer + `<span><a data-page='${prev_page}' id='previous_page_link'>PREVIOUS PAGE</a></span>` + "&emsp;&emsp;&emsp;&emsp;";
    }
    // if page less than total_pages, add link to next page
    if (page < total_pages) {
        const next_page = "" + (parseInt(page) + 1);
        footer = footer + `<span><a data-page='${next_page}' id='next_page_link'>NEXT PAGE</a></span>`;
    }

    innercontent = innercontent + footer;

    return innercontent;
}


function process_tmdb_credits(movieData, creditsData) {
    let detail_innercontent = "<span class='movie_details_title'>" + movieData["title"] + "</span><BR>";

    if (movieData["title"] !== movieData["original_title"]) {
        detail_innercontent = (detail_innercontent
                               + "(orig.: "
                               + movieData["original_title"]
                               + ")<BR><BR>");
    }
    detail_innercontent = (detail_innercontent
                           + "<p>"
                           + movieData["overview"]
                            + "</p>");
    detail_innercontent = (detail_innercontent
                           + "Director: "
                           + creditsData["director"]
                           + "<BR><BR>");
    detail_innercontent = (detail_innercontent
                           + "Starring:<ul>");
    for (const star of creditsData["starring"]) {
        detail_innercontent = (detail_innercontent
                               + "<li>" + star + "</li>");
    }
    detail_innercontent = detail_innercontent + "</ul>";

    return detail_innercontent;
}


// process new viewing form
function process_new_viewing_form(mode, movieData={}) {

    // the form itself
    const newViewingForm = document.querySelector("#new_viewing_form");

    // replace all elements with listeners to clear old listeners
    // (this is horrible isn't it?!)
    const cinemaInputButton = replaceElement(newViewingForm.querySelector("#cinema_radio_input"));
    const videoInputButton = replaceElement(newViewingForm.querySelector("#video_radio_input"));
    const TVInputButton = replaceElement(newViewingForm.querySelector("#tv_input"));
    const streamingInputButton = replaceElement(newViewingForm.querySelector("#streaming_input"));
    const DVDInputButton = replaceElement(newViewingForm.querySelector("#dvd_input"));
    const newViewingSaveButton = replaceElement(document.querySelector("#new_viewing_save_button"));

    // make sure Save button is enabled
    newViewingSaveButton.disabled = false;

    // check if this is an _update_:
    const updateHidden = newViewingForm.querySelector("#viewing_update_hidden");

    var profile_url = "";

    if (mode !== "import") {
        // get url for basic profile view (for navigating
        profile_url = document.querySelector("#profile_movie_list").dataset["profile_url"];
    }

    if (mode === "edit") {
        // query database and populate fields
        const xhr_query_viewing = new XMLHttpRequest();
        let query_url = updateHidden.dataset["query_url"];
        query_url = query_url + `?viewing_id=${updateHidden.value}`
        xhr_query_viewing.open('GET', query_url, false);

        // Set the callback function for when the response is received
        xhr_query_viewing.onload = function() {
            if (xhr_query_viewing.status === 200) {
                console.log(xhr_query_viewing.responseText);
                let viewingData = JSON.parse(xhr_query_viewing.responseText);

                // populate fields in form
                newViewingForm.querySelector("#movie_name_input").value = viewingData.film_title;
                try {
                    newViewingForm.querySelector("#date_input").value = viewingData.date;
                } catch(error) {
                    console.log("invalid date, doing nothing");
                }
                newViewingForm.querySelector("#location_input").value = viewingData.location;
                newViewingForm.querySelector("#cinema_input").value = viewingData.cinema;
                newViewingForm.querySelector("#viewing_comments").value = viewingData.comments;
                newViewingForm.querySelector("#tv_station_input").value = viewingData.tv_channel;
                newViewingForm.querySelector("#streaming_platform_input").value = viewingData.streaming_platform;

                // set hiddenness of conditional rows
                newViewingForm.querySelectorAll(".invisible_table_row").forEach(function(invisibleRow) {
                    invisibleRow.style.display = "none";
                });
                if (viewingData.cinema_or_tv === "Cinema") {
                    newViewingForm.querySelector("#cinema_radio_input").checked = true;
                    newViewingForm.querySelector("#video_radio_input").checked = false;
                    // unhide location and cinema inputs
                    newViewingForm.querySelector("#location_form_row").style.display = "table-row";
                    newViewingForm.querySelector("#cinema_form_row").style.display = "table-row";
                } else if (viewingData.cinema_or_tv === "Video") {
                    newViewingForm.querySelector("#cinema_radio_input").checked = false;
                    newViewingForm.querySelector("#video_radio_input").checked = true;
                    // unhide medium row
                    newViewingForm.querySelector("#medium_row").style.display = "table-row";
                }

                newViewingForm.querySelector("#tv_input").checked = false;
                newViewingForm.querySelector("#streaming_input").checked = false;
                newViewingForm.querySelector("#dvd_input").checked = false;
                if (viewingData.video_medium === "TV") {
                    newViewingForm.querySelector("#tv_input").checked = true;
                    // unhide TV channel
                    newViewingForm.querySelector("#tv_station_row").style.display = "table-row";
                } else if (viewingData.video_medium === "Streaming") {
                    newViewingForm.querySelector("#streaming_input").checked = true;
                    // unhide Streaming input
                    newViewingForm.querySelector("#streaming_platform_row").style.display = "table-row";
                }

            }
        }

        xhr_query_viewing.send();

    } else if (mode === "new") {

        newViewingForm.reset();

        // set tmdb id
        const tmdbIDHidden = newViewingForm.querySelector("#tmdb_id_hidden");
        tmdbIDHidden.value = movieData["tmdb_id"];

        // set movie title
        const movieNameInput = newViewingForm.querySelector("#movie_name_input");
        movieNameInput.value = movieData["title"];

        // set viewing date to today
        const dateInput = newViewingForm.querySelector("#date_input");
        const today = new Date();
        const formattedDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
        dateInput.value = formattedDate;

    } else if (mode == "import") {

        newViewingForm.reset();

        // get viewing data from uploaded file in server session data
        const get_session_data_url = document.querySelector("#new_viewing_form_import_div").dataset["get_session_url"];
        const get_session_data_query = "?key=uploaded_viewings&subkey=" + movieData["import_counter"];

        const xhr_get_session = new XMLHttpRequest();
        xhr_get_session.open("GET", get_session_data_url + get_session_data_query);
        xhr_get_session.onload = function() {
            if (xhr_get_session.status == 200) {
                let responseData = JSON.parse(xhr_get_session.responseText);

                // set fields in form
                newViewingForm.querySelector("#movie_name_input").value = movieData["title"];
                newViewingForm.querySelector("#tmdb_id_hidden").value = movieData["tmdb_id"];

                if ("date" in responseData) {
                    try {
                        newViewingForm.querySelector("#date_input").value = responseData["date"];
                    } catch(error) {
                        console.log("invalid date, doing nothing");
                    }
                }
                if ("cinema_or_tv" in responseData) {
                    if (responseData["cinema_or_tv"] === "Cinema") {
                        newViewingForm.querySelector("#cinema_radio_input").checked = true;
                        newViewingForm.querySelector("#video_radio_input").checked = false;
                    } else if (responseData["cinema_or_tv"] === "Video") {
                        newViewingForm.querySelector("#cinema_radio_input").checked = false;
                        newViewingForm.querySelector("#video_radio_input").checked = true;
                        // unhide medium row
                        newViewingForm.querySelector("#medium_row").style.display = "table-row";
                    }
                }
                if ("location" in responseData) {
                    newViewingForm.querySelector("#location_form_row").style.display = "table-row";
                    newViewingForm.querySelector("#cinema_form_row").style.display = "table-row";
                    newViewingForm.querySelector("#location_input").value = responseData["location"];
                    newViewingForm.querySelector("#cinema_radio_input").checked = true;
                    newViewingForm.querySelector("#video_radio_input").checked = false;
                }
                if ("cinema" in responseData) {
                    newViewingForm.querySelector("#location_form_row").style.display = "table-row";
                    newViewingForm.querySelector("#cinema_form_row").style.display = "table-row";
                    newViewingForm.querySelector("#cinema_input").value = responseData["cinema"];
                    newViewingForm.querySelector("#cinema_radio_input").checked = true;
                    newViewingForm.querySelector("#video_radio_input").checked = false;
                }
                if ("video_medium" in responseData) {
                    // unhide medium row
                    newViewingForm.querySelector("#medium_row").style.display = "table-row";
                    if (responseData["video_medium"] === "TV") {
                        newViewingForm.querySelector("#tv_station_row").style.display = "table-row";
                        newViewingForm.querySelector("#tv_input").checked = true;
                        newViewingForm.querySelector("#streaming_input").checked = false;
                        newViewingForm.querySelector("#dvd_input").checked = false;
                    } else if (responseData["video_medium"] === "Streaming") {
                        newViewingForm.querySelector("#streaming_platform_row").style.display = "table-row";
                        newViewingForm.querySelector("#tv_input").checked = true;
                        newViewingForm.querySelector("#streaming_input").checked = false;
                        newViewingForm.querySelector("#dvd_input").checked = false;
                    } else if (responseData["video_medium"] === "DVD") {
                        newViewingForm.querySelector("#tv_input").checked = false;
                        newViewingForm.querySelector("#streaming_input").checked = false;
                        newViewingForm.querySelector("#dvd_input").checked = true;
                    }
                }
                if ("tv_channel" in responseData) {
                    newViewingForm.querySelector("#cinema_radio_input").checked = false;
                    newViewingForm.querySelector("#video_radio_input").checked = true;
                    // unhide medium row
                    newViewingForm.querySelector("#medium_row").style.display = "table-row";
                    // populate tv_channel, set other known values
                    newViewingForm.querySelector("#tv_station_row").style.display = "table-row";
                    newViewingForm.querySelector("#tv_channel_input").value = responseData["tv_channel"];
                    newViewingForm.querySelector("#cinema_radio_input").checked = false;
                    newViewingForm.querySelector("#video_radio_input").checked = true;
                    newViewingForm.querySelector("#tv_input").checked = true;
                }
                if ("streaming_platform" in responseData) {
                    newViewingForm.querySelector("#cinema_radio_input").checked = false;
                    newViewingForm.querySelector("#video_radio_input").checked = true;
                    // unhide medium row
                    newViewingForm.querySelector("#medium_row").style.display = "table-row";
                    // populate streaming, set other known values.
                    newViewingForm.querySelector("#streaming_platform_row").style.display = "table-row";
                    newViewingForm.querySelector("#streaming_platform_input").value = responseData["streaming_platform"];
                    newViewingForm.querySelector("#cinema_radio_input").checked = false;
                    newViewingForm.querySelector("#video_radio_input").checked = true;
                    newViewingForm.querySelector("#streaming_radio_input").checked = true;
                }
                if ("comments" in responseData) {
                    newViewingForm.querySelector("#viewing_comments").value = responseData["comments"];
                }
            }
        }
        xhr_get_session.send();
    }

    // on selection of "cinema" or "video" radio button, expose appropriate fields
    cinemaInputButton.addEventListener("click", function() {
        // hide all invisible rows
        newViewingForm.querySelectorAll(".invisible_table_row").forEach(function(invisibleRow) {
            invisibleRow.style.display = "none";
        });
        // except
        newViewingForm.querySelector("#location_form_row").style.display = "table-row";
        newViewingForm.querySelector("#cinema_form_row").style.display = "table-row";

        // clear streaming and channel inputs
        newViewingForm.querySelector("#tv_station_input").value = "";
        newViewingForm.querySelector("#streaming_platform_input").value = "";
    });
    videoInputButton.addEventListener("click", function() {
        // hide all invisible rows
        newViewingForm.querySelectorAll(".invisible_table_row").forEach(function(invisibleRow) {
            invisibleRow.style.display = "none";
        });
        // except
        newViewingForm.querySelector("#medium_row").style.display = "table-row";
        // clear location and cinema values
        newViewingForm.querySelector("#location_input").value = "";
        newViewingForm.querySelector("#cinema_input").value = "";
    });
    // same for radio buttons that are hidden at first
    TVInputButton.addEventListener("click", function() {
        newViewingForm.querySelector("#tv_station_row").style.display = "table-row";
        newViewingForm.querySelector("#streaming_platform_row").style.display = "none";
        newViewingForm.querySelector("#streaming_platform_input").value = "";
    });
    streamingInputButton.addEventListener("click", function() {
        newViewingForm.querySelector("#tv_station_row").style.display = "none";
        newViewingForm.querySelector("#tv_station_input").value = "";
        newViewingForm.querySelector("#streaming_platform_row").style.display = "table-row";
    });
    DVDInputButton.addEventListener("click", function() {
        newViewingForm.querySelector("#tv_station_row").style.display = "none";
        newViewingForm.querySelector("#tv_station_input").value = "";
        newViewingForm.querySelector("#streaming_platform_row").style.display = "none";
        newViewingForm.querySelector("#streaming_platform_input").value = "";
    });

    // handle submission of the form
    newViewingSaveButton.addEventListener("click", function(event) {
        event.preventDefault();

        // disable the save button to prevent double submission
        newViewingSaveButton.disabled = true;

        // submit form:
        const new_viewing_url = newViewingSaveButton.dataset["url"];

        // prepare the POST payload
        const formData = new FormData(newViewingForm);
        // console.log(...formData);

        // Create an XMLHttpRequest object
        const xhr_new_viewing = new XMLHttpRequest();
        xhr_new_viewing.open("POST", new_viewing_url, false);

        // Set header data
        xhr_new_viewing.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));

        // Set the callback function for when the response is received
        xhr_new_viewing.onload = function() {
            if (xhr_new_viewing.status === 200) {
                // reset form and close Modal bzw. import form
                newViewingForm.reset();

                if (mode === "import") {
                    document.querySelector("#new_viewing_form_import_div").style.display = "none";

                    // make _synchronous_ POST request to update the "validated" viewing status
                    const xhr_validate = new XMLHttpRequest();

                    const validate_url = document.querySelector("#new_viewing_form_import_div").dataset["import_url"];
                    xhr_validate.open("POST", validate_url, false);
                    xhr_validate.setRequestHeader("Content-Type", "application/json");
                    xhr_validate.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
                    console.log(JSON.stringify({
                        validated: movieData["import_counter"]
                    }));
                    xhr_validate.send(JSON.stringify({
                        validated: movieData["import_counter"]
                    }));
                    if (xhr_validate.status === 200) {
                       console.log("That's what you say!!!");
                       // do an ajax request to get "uploaded_viewings" from session
                       // and edit the "validated" indicator accordingly in the DOM
                       //
                       // modify the just-validated title to look and work like it
                       // will once page refreshes
                       const import_counter = movieData["import_counter"];
                       const theTitle = document.querySelector(`.uploaded_title[data-counter="${import_counter}"]`);
                       theTitle.querySelector(".validated_indicator").innerHTML = "&#x2713;";
                       // change the class to change the colour
                       theTitle.setAttribute("class", "uploaded_title validated_title");
                       // change the background colour (since it's no longer in the array of titles)
                       theTitle.style.backgroundColor = "inherit";
                       // reset the element to remove the listener
                       replaceElement(theTitle);
                    } else {
                       throw new Error('Request failed: ' + xhr_validate.statusText);
                    }

                } else {
                    // new viewing bzw. edit viewing mode

                    document.querySelector("#new_viewing_form_modal").style.display = "none";
                    document.querySelector("#modal_overlay").style.display = "none";
                    // navigate (back) to index view
                    window.location.replace(profile_url);
                }
            }
        }

        xhr_new_viewing.send(formData);
    });
}

