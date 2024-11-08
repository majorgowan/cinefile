document.addEventListener("DOMContentLoaded", function() {

    // variables for modals that will be shown and hidden as needed
    // for movie search
    const modalOverlay = document.querySelector("#modal_overlay");
    const tmdbSearchModal = document.querySelector("#tmdb_search_modal");
    // for detail on a search result (with option to Select it)
    const tmdbDetailModal = document.querySelector("#tmdb_detail_modal");
    const tmdbDetailModalContent = document.querySelector("#tmdb_detail_modal_content");
    // form for adding a new Viewing of the selected movie
    const newViewingFormModal = document.querySelector("#new_viewing_form_modal");
    const newViewingForm = newViewingFormModal.querySelector("#new_viewing_form");

    // divs holding viewings
    const viewingEditButtons = document.querySelectorAll(".viewing_edit_button");
    const viewingTMDBButtons = document.querySelectorAll(".viewing_row .tmdb_link_div img");
    const viewingOverviewLinks = document.querySelectorAll(".overview_link");

    // on user clicking "Add" in the sidebar, open the search modal
    const addViewingLink = document.querySelector("#add_viewing_link");
    if (addViewingLink != null) {
        addViewingLink.onclick = (event) => {
            event.preventDefault();
            // clear the search bar and results
            document.querySelector("#tmdb_search_text").value = "";
            document.querySelector("#tmdb_search_results").innerHTML = "";
            document.querySelector("#tmdb_search_results").style.display = "none";
            modalOverlay.style.display = "block";
            tmdbSearchModal.style.display = "block";
        }
    }

    // search bar for TMDB title search
    const tmdbSearchText = document.querySelector("#tmdb_search_text");
    const tmdbSearchSearchButton = document.querySelector("#tmdb_search_search_button");
    // close buttons (x in top right corner)
    const tmdbSearchClose = tmdbSearchModal.querySelector(".close");
    const tmdbDetailClose = tmdbDetailModal.querySelector(".close");
    const newViewingClose = newViewingFormModal.querySelector(".close");
    // select button for accepting movie from search results
    const tmdbDetailSelect = tmdbDetailModal.querySelector("#tmdb_detail_select_button");
    // div with search results (to be populated with return from TMDB API)
    const tmdbSearchResults = document.querySelector("#tmdb_search_results");

    // get urls for API searches  from search data tag in template
    const search_url = tmdbSearchText.dataset["url"];
    const credits_url = tmdbSearchText.dataset["credits_url"];

    // process search-tmdb form
    function search_tmdb(search_pattern, results_page) {
        const searchParams = new URLSearchParams({
            "pattern": encodeURIComponent(search_pattern),
            "page": results_page
        });
        let full_url = search_url + "?" + searchParams.toString();

        // Create an XMLHttpRequest object
        const xhr = new XMLHttpRequest();
        xhr.open('GET', full_url, true);

        // Set the callback function for when the response is received
        xhr.onload = function() {
            if (xhr.status === 200) {
                // Process the response data
                let searchData = JSON.parse(xhr.responseText);
                let innercontent = process_tmdb_search(searchData);

                // clean query string (otherwise gets contaminated with %blahblah)
                const decodedQuery = decodeURIComponent(searchData["query"]);

                // add to div and unhide results
                tmdbSearchResults.innerHTML = innercontent;
                tmdbSearchResults.style.display = "block";

                // add listeners to Next bzw. Previous page links:
                const previousPageLink = document.querySelector("#previous_page_link");
                const nextPageLink = document.querySelector("#next_page_link");

                if (previousPageLink !== null) {
                    previousPageLink.addEventListener("click", function() {
                        search_tmdb(decodedQuery, previousPageLink.dataset["page"]);
                    });
                }
                if (nextPageLink !== null) {
                    nextPageLink.addEventListener("click", function() {
                        search_tmdb(decodedQuery, nextPageLink.dataset["page"]);
                    });
                }

                // add listener to each search result link
                const search_links = document.querySelectorAll(".movie_search_link");
                search_links.forEach((search_link) => {
                    search_link.addEventListener("click", function() {
                        const xhr_credits = new XMLHttpRequest();
                        const movie_id = search_link.dataset["movie_id"];
                        const full_credits_url = credits_url + "?movie_id=" + movie_id;
                        xhr_credits.open('GET', full_credits_url, true);

                        xhr_credits.onload = function() {
                            if (xhr_credits.status === 200) {
                                // show detail modal
                                tmdbDetailModal.style.display = "block";
                                let creditsData = JSON.parse(xhr_credits.responseText);

                                let movieData = searchData["candidates"][movie_id];
                                movieData["tmdb_id"] = movie_id;
                                let detail_innercontent = process_tmdb_credits(movieData, creditsData);

                                tmdbDetailModalContent.innerHTML = detail_innercontent;

                                // on clicking Select in detail modal, open New Viewing modal and process
                                tmdbDetailSelect.addEventListener("click", function() {

                                    // close everything and show viewing form!
                                    tmdbDetailModal.style.display = "none";
                                    tmdbSearchModal.style.display = "none";
                                    newViewingFormModal.style.display = "block";

                                    process_new_viewing_form("new", movieData);

                                });
                            }
                        }

                        // Send the request
                        xhr_credits.send();
                    });
                });

            }
        };
        // Send the request
        xhr.send();
    }

    // add event listeners to trigger modal opening and closing etc.

    // run TMDB search
    function tmdbSearchGo(event) {
            // get search text
            let search_pattern = tmdbSearchText.value;
            const results_page = tmdbSearchText.dataset["page"];
            search_tmdb(search_pattern, results_page);
    }
    // allow either clicking search or pressing Enter
    tmdbSearchSearchButton.addEventListener("click", tmdbSearchGo);
    tmdbSearchText.addEventListener("keyup", function(event) {
        if (event.keyCode === 13) {
            tmdbSearchGo(event);
        }
    });

    // event listener for tmdb button
    document.querySelector("#tmdb_link_button").addEventListener("click", function() {
        window.open("https://www.themoviedb.org/movie/184314", "_blank");
    });

    // event listener for editing viewings
    viewingEditButtons.forEach(function(editButton) {
        editButton.addEventListener("click", function(event) {
            // handle click event for each div
            let viewing_id = editButton.dataset["viewing_id"];
            // set hidden input "viewing_update_hidden" to "update":
            newViewingForm.querySelector("#viewing_update_hidden").value = viewing_id;
            // make overlay visible
            modalOverlay.style.display = "block";
            // show new-form modal
            newViewingFormModal.style.display = "block";
            process_new_viewing_form("edit");
        });
    });

    // event listener for TMDB links in Viewings
    viewingTMDBButtons.forEach(function(tmdbButton) {
        tmdbButton.addEventListener("click", function(event) {
            // handle click event for each div
            let button_tmdb_id = tmdbButton.dataset["tmdb_id"];
            let tmdb_url = "https://www.themoviedb.org/movie/" + button_tmdb_id;
            window.open(tmdb_url, "_blank");
        });
    });

    // event listener for Overview links in Viewings (default to hide overview)
    viewingOverviewLinks.forEach(function(overviewLink) {
        overviewLink.addEventListener("click", function(event) {
            // get the corresponding overview span and toggle its class
            const overviewSpan = document.getElementById(overviewLink.dataset["overview_id"]);
            if (overviewSpan.className == "hidden_overview") {
                overviewSpan.className = "shown_overview";
                overviewLink.innerHTML = "hide tmdb overview";
            } else {
                overviewSpan.className = "hidden_overview";
                overviewLink.innerHTML = "show tmdb overview";
            }
        });
    });

    // implement close buttons
    tmdbSearchClose.addEventListener("click", function() {
        tmdbSearchModal.style.display = "none";
        modalOverlay.style.display = "none";
    });
    tmdbDetailClose.addEventListener("click", function() {
        tmdbDetailModal.style.display = "none";
    });
    newViewingClose.addEventListener("click", function() {
        newViewingFormModal.style.display = "none";
        modalOverlay.style.display = "none";
    });

});
