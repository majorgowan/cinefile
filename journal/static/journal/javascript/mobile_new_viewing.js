document.addEventListener("DOMContentLoaded", function() {

    // implement Cancel button in forms
    const cancelButton = document.querySelector(".cancel_button");
    const cancel_url = cancelButton.dataset["cancel_url"];
    cancelButton.onclick = function() {
        window.location.replace(cancel_url);
    }

    // implement Media selector
    const videoMediumSelect = document.querySelector("#id_video_medium");
    const tvChannelInput = document.querySelector("#id_tv_channel");
    const streamingPlatformInput = document.querySelector("#id_streaming_platform");
    if (videoMediumSelect != null) {
        // initial settings (for edit case)
        let vmsValue = videoMediumSelect.options[videoMediumSelect.selectedIndex].value;
        if (vmsValue === "TV") {
            tvChannelInput.disabled = false;
            streamingPlatformInput.disabled = true;
        } else if (vmsValue === "Streaming") {
            tvChannelInput.disabled = true;
            streamingPlatformInput.disabled = false;
        }
        videoMediumSelect.addEventListener("change", function(event) {
            vmsValue = videoMediumSelect.options[videoMediumSelect.selectedIndex].value;
            if (vmsValue === "TV") {
                tvChannelInput.disabled = false;
                streamingPlatformInput.disabled = true;
                streamingPlatformInput.value = "";
            } else if (vmsValue === "Streaming") {
                tvChannelInput.disabled = true;
                tvChannelInput.value = "";
                streamingPlatformInput.disabled = false;
            } else {
                // it's a DVD or Video
                tvChannelInput.disabled = true;
                tvChannelInput.value = "";
                streamingPlatformInput.disabled = true;
                streamingPlatformInput.value = "";
            }
        });
    }

    // implement Delete Viewing button
    const deleteViewingButton = document.querySelector("#mobile_delete_viewing_button");
    if (deleteViewingButton != null) {

        deleteViewingButton.onclick = function() {
            // make POST request to "delete_viewing" view with viewingID as payload
            const delete_viewing_url = deleteViewingButton.dataset["delete_url"];
            const cancel_url = deleteViewingButton.dataset["cancel_url"];
            const viewing_id_to_delete = deleteViewingButton.dataset["viewing_id"];

            // Create an XMLHttpRequest object
            const xhr_delete_viewing = new XMLHttpRequest();
            xhr_delete_viewing.open("POST", delete_viewing_url, false);

            // Set header data
            xhr_delete_viewing.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
            xhr_delete_viewing.setRequestHeader('Content-Type', 'application/json');

            // Set the callback function for when the response is received
            xhr_delete_viewing.onload = function() {
                // navigate (back) to index view
                window.location.replace(cancel_url);
            }

            xhr_delete_viewing.send(JSON.stringify({
                viewing_id: viewing_id_to_delete
            }));
        }
    }
});

