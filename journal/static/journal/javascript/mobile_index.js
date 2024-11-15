document.addEventListener("DOMContentLoaded", function() {

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
        mobileAddViewingModal.setAttribute("class", "mobile_modal_visible");
        // hide the menu
        navMenu.style.display = "none";
    }
    mobileAddViewingModalClose.onclick = function() {
        mobileAddViewingModal.setAttribute("class", "mobile_modal_invisible");
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




});