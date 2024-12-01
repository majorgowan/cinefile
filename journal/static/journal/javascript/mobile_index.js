document.addEventListener("DOMContentLoaded", function() {

    // implement TMDB links in Viewings
    const viewingTMDBButtons = document.querySelectorAll(".viewing_row .tmdb_link_div img");
    viewingTMDBButtons.forEach(function(tmdbButton) {
        tmdbButton.addEventListener("click", function(event) {
            // handle click event for each div
            let button_tmdb_id = tmdbButton.dataset["tmdb_id"];
            let tmdb_url = "https://www.themoviedb.org/movie/" + button_tmdb_id;
            window.open(tmdb_url, "_blank");
        });
    });

    // implement overview show/hide
    const viewingOverviewLinks = document.querySelectorAll(".overview_link");
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

    // implement spoiler show/hide
    const viewingSpoilersLinks = document.querySelectorAll(".spoilers_link");
    // event listener for Spoilers links in Viewings (default to hide spoilers)
    viewingSpoilersLinks.forEach(function(spoilersLink) {
        spoilersLink.addEventListener("click", function(event) {
            // get the corresponding comment span and toggle its class
            const commentsSpan = document.getElementById(spoilersLink.dataset["comments_id"]);
            if (commentsSpan.className == "hidden_comments") {
                commentsSpan.className = "shown_comments";
                spoilersLink.innerHTML = "hide comments";
            } else {
                commentsSpan.className = "hidden_comments";
                spoilersLink.innerHTML = "show comments";
            }
        });
    });

    // navigation menu dynamics
    const navMenu = document.getElementById("nav_menu");

    const menuMyCinefileItem = document.getElementById("menu_my_cinefile_item");
    if (menuMyCinefileItem != null) {
        my_cinefile_url = menuMyCinefileItem.dataset["url"];
        menuMyCinefileItem.onclick = function() {
            window.location.replace(my_cinefile_url);
        }
    }

    const menuAddViewingItem = document.getElementById("menu_add_viewing_item");
    const mobileAddViewingModal = document.getElementById("mobile_add_viewing_modal");
    const mobileAddViewingModalClose = mobileAddViewingModal.querySelector(".close");

    menuAddViewingItem.onclick = function() {
        mobileAddViewingModal.setAttribute("class", "mobile_modal mobile_modal_visible");
        // hide the menu
        navMenu.style.display = "none";
    }
    mobileAddViewingModalClose.onclick = function() {
        tmdbSearchText.value = "";
        tmdbSearchResults.innerHTML = "";
        mobileAddViewingModal.setAttribute("class", "mobile_modal mobile_modal_invisible");
    }

    // implement "Follow / Unfollow" function
    const followLink = document.querySelector('[id$="follow_item"]');
    // if user not logged in, then there won't be a follow link
    if (followLink != null) {
        followLink.onclick = (event) => {

            const follow_url = followLink.dataset["follow_url"];
            const follower_name = followLink.dataset["follower"];
            const followed_name = followLink.dataset["followed"];

            let follow_action;
            const followLink_text = followLink.innerHTML;
            if (followLink_text.startsWith("Un")) {
                follow_action = "unfollow";
            } else {
                follow_action = "follow";
            }

            const xhr_follow = new XMLHttpRequest();
            xhr_follow.open("POST", follow_url, true);

            // Set header data
            xhr_follow.setRequestHeader("Content-Type", "application/json");
            xhr_follow.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));

            xhr_follow.send(JSON.stringify({
                follower: follower_name,
                followed: followed_name,
                action: follow_action
            }));

            // Set the callback function for when the response is received
            xhr_follow.onload = function() {
                if (xhr_follow.status === 200) {
                    // Process the response data

                    // if success toggle the follow / unfollow
                    if (followLink_text.startsWith("Un")) {
                        followLink.innerHTML = followLink_text.replace("Unfollow", "Follow");
                    } else {
                        followLink.innerHTML = followLink_text.replace("Follow", "Unfollow");
                    }

                    // console.log(JSON.parse(xhr_follow.responseText));
                }
            }
        }
    }


    // implement "new viewing" modal
    const tmdbSearchModal = document.getElementById("mobile_add_viewing_modal");
    const mobileMovieTitleForm = document.getElementById("mobile_movie_title_form");
    const tmdbSearchText = document.getElementById("mobile_tmdb_search_text_input");
    // deprecating the button!
    // const tmdbSearchSearchButton = document.getElementById("tmdb_search_search_button");
    const tmdbSearchResults = document.getElementById("mobile_tmdb_search_results");
    const tmdbDetailModal = document.getElementById("mobile_movie_detail_modal");
    const tmdbDetailModalContent = document.getElementById("mobile_tmdb_detail_modal_content");
    const tmdbDetailModalClose = tmdbDetailModal.querySelector(".close");
    const tmdbDetailSelectCinema = tmdbDetailModal.querySelector("#tmdb_detail_select_cinema_button");
    const tmdbDetailSelectVideo = tmdbDetailModal.querySelector("#tmdb_detail_select_video_button");
    const search_url = tmdbSearchText.dataset["url"];
    const credits_url = tmdbSearchText.dataset["credits_url"];

    tmdbDetailModalClose.addEventListener("click", function() {
        tmdbDetailModal.setAttribute("class", "mobile_modal mobile_modal_invisible");
    });


    if (mobileMovieTitleForm != null) {

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

                    // style the list
                    tmdbSearchResults.querySelector("ul").classList.add("mobile_scrolling_list");
                    tmdbSearchResults.querySelector("ul").style.height = "330px";
                    tmdbSearchResults.querySelector("ul").style.marginBottom = "20px";

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
                                    tmdbDetailModal.setAttribute("class", "mobile_modal mobile_modal_visible");
                                    let creditsData = JSON.parse(xhr_credits.responseText);

                                    let movieData = searchData["candidates"][movie_id];
                                    movieData["tmdb_id"] = movie_id;
                                    let detail_innercontent = process_tmdb_credits(movieData, creditsData);

                                    tmdbDetailModalContent.innerHTML = detail_innercontent;

                                    // on clicking Select in detail modal, open New Viewing modal and process
                                    tmdbDetailSelectCinema.addEventListener("click", function() {

                                        // show viewing form!
                                        const new_viewing_form_url = tmdbDetailSelectCinema.dataset["url"];
                                        window.location.replace(new_viewing_form_url);
                                    });
                                    tmdbDetailSelectVideo.addEventListener("click", function() {

                                        // show viewing form!
                                        const new_viewing_form_url = tmdbDetailSelectVideo.dataset["url"];
                                        window.location.replace(new_viewing_form_url);
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

        function tmdbSearchGo(event) {
            let search_pattern = tmdbSearchText.value;
            const results_page = tmdbSearchText.dataset["page"];
            search_tmdb(search_pattern, results_page);
        }

        // add listeners to text input (and button -- DEPRECATED)
        // tmdbSearchSearchButton.addEventListener("click", tmdbSearchGo);
        tmdbSearchText.addEventListener("keyup", function(event) {
            if (event.keyCode === 13) {
                tmdbSearchGo(event);
            }
        });

    }

});