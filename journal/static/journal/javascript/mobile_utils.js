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
});

