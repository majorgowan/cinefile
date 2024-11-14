document.addEventListener("DOMContentLoaded", function() {

    const mobileMenuSymbol = document.getElementById("mobile_menu_symbol");
    const navMenu = document.getElementById("nav_menu");
    mobileMenuSymbol.onclick = function() {
        if (navMenu.style.display === "block") {
            navMenu.style.display = "none";
        } else {
            navMenu.style.display = "block";
        }
    };

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

    const menuAboutItem = document.getElementById("menu_about_item");
    const mobileAboutModal = document.getElementById("mobile_about_modal");
    const mobileAboutModalClose = mobileAboutModal.querySelector(".close");

    menuAboutItem.onclick = function() {
        mobileAboutModal.setAttribute("class", "mobile_modal_visible");
        // hide the menu
        navMenu.style.display = "none";
    }
    mobileAboutModalClose.onclick = function() {
        mobileAboutModal.setAttribute("class", "mobile_modal_invisible");
    }


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


    const menuViewAnotherItem = document.getElementById("menu_view_another_item");
    const mobileViewAnotherModal = document.getElementById("mobile_view_another_modal");
    const mobileViewAnotherModalClose = mobileViewAnotherModal.querySelector(".close");

    menuViewAnotherItem.onclick = function() {
        mobileViewAnotherModal.setAttribute("class", "mobile_modal_visible");
        // hide the menu
        navMenu.style.display = "none";
    }
    mobileViewAnotherModalClose.onclick = function() {
        mobileViewAnotherModal.setAttribute("class", "mobile_modal_invisible");
    }




});