// Check If Friend Has Seen Message
setInterval(function () {
    seen_elements = document.querySelectorAll("[data-seen='false']");
    if (seen_elements.length > 0) {
        $.ajax({
            type: 'GET',
            url: seen_check_api + "/" + $("#current_user").text(),
            data: {},
            success: function (seen) {
                seen = seen.seen;

                if (seen == true && seen_elements.length > 0) {
                    for (i = 0; i < seen_elements.length; i++) {

                        seen_element = seen_elements[i];

                        seen_element.setAttribute("data-seen", "true");
                        getSeen(seen_element);

                    }
                }

            }
        })
    }
}, 1000);