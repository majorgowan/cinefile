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
                           + "<p class='movie_details_overview'>"
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
