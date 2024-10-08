document.addEventListener("DOMContentLoaded", function() {

    // the panel to display titles list
    const importViewingList = document.querySelector("#import_viewing_list");
    // the panel to display tmdb search and viewing forms
    const importViewingDetail = document.querySelector("#import_viewing_detail_div");
    const importSearchResults = document.querySelector("#import_search_results_div");
    const importSearchResultsContent = document.querySelector("#import_search_results_content");
    // variables for the imported title links
    const uploadedTitles = document.querySelectorAll(".uploaded_title.unvalidated_title");
    // text input for modifying title search
    const tmdbSearchTextInput = document.querySelector("#tmdb_search_text_import");
    // for the detail modal
    const tmdbDetailModal = document.querySelector("#tmdb_detail_modal");
    const tmdbDetailModalContent = document.querySelector("#tmdb_detail_modal_content");
    const tmdbDetailClose = tmdbDetailModal.querySelector(".close");
    // for new viewing form
    const newViewingFormImport = document.querySelector("#new_viewing_form_import_div");
    const newViewingFormClose = newViewingFormImport.querySelector(".close");

    // URL for searching TMDB
    const search_url = importSearchResults.dataset["url"];
    const credits_url = importSearchResults.dataset["credits_url"];

    // variable for currently selected viewing in list
    var counter;

    // implement select element to load previously uploaded file
    const uploadedFileChooser = document.querySelector("#uploaded_file_chooser");
    if (uploadedFileChooser != undefined) {
        uploadedFileChooser.addEventListener("change", function(event) {
            const chosen_value = event.target.value;
            const import_tool_url = event.target.dataset["import_url"];
            // prepare GET request
            const searchParams = new URLSearchParams({
                "filename": encodeURIComponent(chosen_value)
            });
            const full_url = import_tool_url + "?" + searchParams.toString();
            window.location.replace(full_url);
        });
    }

    function search_tmdb_import(search_pattern, results_page, counter) {
        const searchParams = new URLSearchParams({
            "pattern": encodeURIComponent(search_pattern),
            "page": "" + results_page
        });
        const full_url = search_url + "?" + searchParams.toString();

        const xhr_search = new XMLHttpRequest();
        xhr_search.open("GET", full_url, true);

        xhr_search.onload = function() {
            if (xhr_search.status === 200) {

                let searchData = JSON.parse(xhr_search.responseText);
                let innercontent = process_tmdb_search(searchData);

                // add to div and unhide
                importSearchResultsContent.innerHTML = innercontent;
                importSearchResults.style.display = "block";

                // add listeners to Next bzw. Previous page links:
                const previousPageLink = document.querySelector("#previous_page_link");
                const nextPageLink = document.querySelector("#next_page_link");
                if (previousPageLink !== null) {
                    previousPageLink.addEventListener("click", function() {
                        search_tmdb_import(searchData["query"], previousPageLink.dataset["page"]);
                    });
                }
                if (nextPageLink !== null) {
                    nextPageLink.addEventListener("click", function() {
                        search_tmdb_import(searchData["query"], nextPageLink.dataset["page"]);
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
                                movieData["import_counter"] = counter;
                                let detail_innercontent = process_tmdb_credits(movieData, creditsData);

                                tmdbDetailModalContent.innerHTML = detail_innercontent;

                                // on clicking Select in detail modal, open New Viewing modal and process
                                const tmdbDetailSelect = replaceElement(tmdbDetailModal.querySelector("#tmdb_detail_select_button"));
                                tmdbDetailSelect.addEventListener("click", function() {

                                    // close everything and show viewing form!
                                    tmdbDetailModal.style.display = "none";
                                    importSearchResults.style.display = "none";

                                    newViewingFormImport.style.display = "block";
                                    process_new_viewing_form("import", movieData);

                                    // TODO: after processing form (if successful), change "validated" field to true
                                    // or remove from list ... maybe better?

                                    // TODO: manual override for film outside TMDB!

                                });
                            }
                        }

                        // Send the request
                        xhr_credits.send();
                    });
                });

            }
        }

        xhr_search.send();

    }


    // clicking on a viewing shows its details in importViewingDetail panel
    uploadedTitles.forEach(function(uploadedTitle) {
        uploadedTitle.addEventListener("click", function() {

            // close modal if open
            tmdbDetailModal.style.display = "none";
            // hide new viewing form
            newViewingFormImport.style.display = "none";
            // set title's background (and revert all other)
            uploadedTitles.forEach(function(ut) {
                ut.style.backgroundColor = "inherit";
            });
            uploadedTitle.style.backgroundColor = "lightsteelblue";

            let search_pattern = uploadedTitle.querySelector(".viewing_title").innerHTML.trim();
            let results_page = 1;
            counter = uploadedTitle.dataset["counter"];

            // prefill search bar with the title
            tmdbSearchTextInput.value = search_pattern;

            search_tmdb_import(search_pattern, results_page, counter);

        });
    });

    // implement text input to revise search
    tmdbSearchTextInput.addEventListener("keyup", function(event) {
        if (event.keyCode === 13) {
            // get search text
            search_pattern = tmdbSearchTextInput.value;
            results_page = 1;
            search_tmdb_import(search_pattern, results_page, counter);
        }
    });

    // close buttons
    tmdbDetailClose.addEventListener("click", function() {
        tmdbDetailModal.style.display = "none";
    });
    newViewingFormClose.addEventListener("click", function() {
        newViewingFormImport.style.display = "none";
    });

});
