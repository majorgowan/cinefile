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

    const menuViewAnotherItem = document.getElementById("menu_view_another_item");
    // same thing but for not-logged in user (code duplication, sorry)
    const menuViewACinefileItem = document.getElementById("menu_view_a_cinefile_item");
    const mobileViewAnotherModal = document.getElementById("mobile_view_another_modal");
    const mobileViewAnotherModalClose = mobileViewAnotherModal.querySelector(".close");
    if (menuViewAnotherItem != null) {
        menuViewAnotherItem.onclick = function() {
            mobileViewAnotherModal.setAttribute("class", "mobile_modal_visible");
            // hide the menu
            navMenu.style.display = "none";
        }
        mobileViewAnotherModalClose.onclick = function() {
            mobileViewAnotherModal.setAttribute("class", "mobile_modal_invisible");
        }
    }
    if (menuViewACinefileItem != null) {
        menuViewACinefileItem.onclick = function() {
            mobileViewAnotherModal.setAttribute("class", "mobile_modal_visible");
            // hide the menu
            navMenu.style.display = "none";
        }
        mobileViewAnotherModalClose.onclick = function() {
            mobileViewAnotherModal.setAttribute("class", "mobile_modal_invisible");
        }
    }

});

