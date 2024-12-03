document.addEventListener("DOMContentLoaded", function() {

    const mobileMenuSymbol = document.getElementById("mobile_menu_symbol");
    const navMenu = document.getElementById("nav_menu");
    mobileMenuSymbol.onclick = function() {
        if (navMenu.style.display === "block") {
            navMenu.style.display = "none";
            mobileMenuSymbol.style.background = "inherit";
        } else {
            navMenu.style.display = "block";
            mobileMenuSymbol.style.background = "sandybrown";
        }
    };

    const menuAboutItem = document.getElementById("menu_about_item");
    const mobileAboutModal = document.getElementById("mobile_about_modal");
    const mobileAboutModalClose = mobileAboutModal.querySelector(".close");
    menuAboutItem.onclick = function() {
        mobileAboutModal.setAttribute("class", "mobile_modal mobile_modal_visible");
        // hide the menu
        navMenu.style.display = "none";
    }
    mobileAboutModalClose.onclick = function() {
        mobileAboutModal.setAttribute("class", "mobile_modal mobile_modal_invisible");
    }

    const menuViewAnotherItem = document.getElementById("menu_view_another_item");
    // same thing but for not-logged in user (code duplication, sorry)
    const menuViewACinefileItem = document.getElementById("menu_view_a_cinefile_item");
    const mobileViewAnotherModal = document.getElementById("mobile_view_another_modal");
    const mobileViewAnotherModalClose = mobileViewAnotherModal.querySelector(".close");
    // for the search functionality:
    const mobileCinefileMatchesList = document.getElementById("mobile_cinefile_matches_list");
    const viewAnotherSearchTextInput = document.getElementById("view_another_search_text");
    // DEPRECATED
    // const viewAnotherSearchButton = document.getElementById("mobile_view_another_search");

    if (menuViewAnotherItem != null) {
        menuViewAnotherItem.onclick = function() {
            mobileViewAnotherModal.setAttribute("class", "mobile_modal mobile_modal_visible");
            // hide the menu
            navMenu.style.display = "none";
        }
        mobileViewAnotherModalClose.onclick = function() {
            mobileViewAnotherModal.setAttribute("class", "mobile_modal mobile_modal_invisible");
            mobileCinefileMatchesList.innerHTML = "";
            viewAnotherSearchTextInput.value = "";
        }
    }
    if (menuViewACinefileItem != null) {
        menuViewACinefileItem.onclick = function() {
            mobileViewAnotherModal.setAttribute("class", "mobile_modal mobile_modal_visible");
            // hide the menu
            navMenu.style.display = "none";
        }
        mobileViewAnotherModalClose.onclick = function() {
            mobileViewAnotherModal.setAttribute("class", "mobile_modal mobile_modal_invisible");
            mobileCinefileMatchesList.innerHTML = "";
            viewAnotherSearchTextInput.value = "";
        }
    }

    // implement the search for users
    if (viewAnotherSearchTextInput != null) {

        function find_users(find_users_search_string) {
            const find_users_url = viewAnotherSearchTextInput.dataset["find_users_url"];
            const profile_url = viewAnotherSearchTextInput.dataset["profile_url"];
            const xhr_find_users = new XMLHttpRequest();

            const find_users_query_url = find_users_url + `?username=${find_users_search_string}`;
            xhr_find_users.open('GET', find_users_query_url, false);

            xhr_find_users.onload = function() {
                if (xhr_find_users.status === 200) {
                    let matching_users = JSON.parse(xhr_find_users.responseText)["matching_users"];
                    let list_content = "";
                    for (matching_user of matching_users) {
                         list_content += `<li><a href="${profile_url}${matching_user}">${matching_user}</a></li>`;
                    }

                    mobileCinefileMatchesList.innerHTML = list_content;
                }
            }

            xhr_find_users.send();
        }

        viewAnotherSearchTextInput.addEventListener("keyup", function(event) {
            if (event.keyCode === 13) {
                find_users(viewAnotherSearchTextInput.value);
            }
        });
        /* DEPRECATED!!
        viewAnotherSearchButton.addEventListener("click", function(event) {
            find_users(viewAnotherSearchTextInput.value);
        });*/
    }

});

