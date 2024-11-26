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

});

