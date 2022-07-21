var isHTML = RegExp.prototype.test.bind(/(<([^>]+)>)/i);


// Function To Detect URL in Users Messages and Make Them Clickable <a href="https://www.google.com"> href element in the Link
function URLify(string) {
    const urls = string.match(/((((ftp|https?):\/\/)|(w{3}\.))[\-\w@:%_\+.~#?,&\/\/=]+)/g);
    if (urls) {
        urls.forEach(function (url) {

            string = string.replace(url, '<a target="_blank" id="messageUrl" href="' + url + '">' + url + "</a>");

        });
    }
    return string.replace("(", "<br/>(");
}







// Ajax Method to Change the page and Get Another Page of Messages
function reloadChatArea(page_id) {
    if (page_id != $(".active").attr("data-userid")) {
        $('#loadMoreMessagesButton').hide();
        window.history.pushState("/messages/" + page_id + "/#", 'Geekshub', "/messages/" + page_id + "/");


        if ($('.chat-msg').length != 0) {
            $(".chat-msg").remove();
        }

        $.ajax({
            url: friends_Lunch_api + "/" + page_id + "?page=" + 1,
            type: "GET",
            data: {},
            cache: false,
            success: function (MessagesJson) {
                $(".chat-area-title").html(MessagesJson.current_username);
                $(".chat-area-profile").attr("src", MessagesJson.current_username_picture)
                if (MessagesJson.msgs.length != 0) {
                    if (MessagesJson.paginate.has_next == true) {
                        msgs_paginate = MessagesJson.paginate.next_page;
                        if ($("#loadMoreMessagesButton").is(":hidden")) {
                            $("#loadMoreMessagesButton").show();
                            $("#loadMoreMessagesButton").removeAttr("style")

                        }
                    }
                    else {
                        $('#loadMoreMessagesButton').hide();
                    }

                    for (let i = 0; i < MessagesJson.msgs.length; i++) {


                        let msgs = MessagesJson.msgs[i];
                        let msg = msgs.msg;
                        let from_user = msgs.from_user;

                        // Make <a href="https://www.google.com"> if thir a link
                        if (isHTML(msg) == false) {
                            msg = URLify(msg);
                        } else {
                            msg = msg;
                        }


                        if (from_user != request_user_id) {
                            $('#Messages_List').prepend('<div class="chat-msg not-owner"><div class="chat-msg-profile"><div class="chat-msg-date" data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></div></div><div class="chat-msg-content"><div class="chat-msg-text" data-id="' + msgs.id + '">' + msg + '</div></div></div>')
                        } else {
                            $('#Messages_List').prepend('<div class="chat-msg owner"><div class="chat-msg-profile"><div class="chat-msg-date"><span data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></span><span data-seen="' + msgs.seen + '"></span></div></div><div class="chat-msg-content"><div class="chat-msg-text" data-id="' + msgs.id + '">' + msg + '</div></div></div>')
                        }

                        getDate(document.querySelectorAll('[data-dateid="' + msgs.id + '"]'));
                        getSeen(document.querySelectorAll("[data-seen]"));

                        document.querySelector('[data-userid="' + page_id + '"]').classList.remove("online");


                    }
                    $("#chat-area").scrollTop($("#chat-area")[0].scrollHeight);
                }

            }
        });

        try {
            active_element = document.getElementsByClassName("msg active");

            for (let i = 0; i < active_element.length; i++) {
                active_element[i].classList.remove("active");
            }
        } catch (error) {
        }
        document.querySelector('[data-userid="' + page_id + '"]').classList.add('active');
        $("#current_user").text(page_id);

    }
}


var msgs_paginate = 2;
// Ajax Method To Load More Messages
function loadMoreMessagesButton() {

    $.ajax({
        url: $("#messages_home_api").text() + "/" + $("#current_user").text() + "?page=" + msgs_paginate,
        type: "GET",
        data: {},
        cache: false,
        success: function (MessagesJson) {

            if (MessagesJson.paginate.has_next == true) {
                msgs_paginate = MessagesJson.paginate.next_page;
            }
            else {
                msgs_paginate = 2;
                $('#loadMoreMessagesButton').hide();
            }



            for (let i = 0; i < MessagesJson.msgs.length; i++) {

                let msgs = MessagesJson.msgs[i];
                let msg = msgs.msg;
                let from_user = msgs.from_user;

                // Make <a href="https://www.google.com"> if thir a link
                if (isHTML(msg) == false) {
                    msg = URLify(msg);
                } else {
                    msg = msg;
                }


                if (from_user != request_user_id) {
                    $('#Messages_List').prepend('<div class="chat-msg not-owner"><div class="chat-msg-profile"><div class="chat-msg-date" data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></div></div><div class="chat-msg-content"><div class="chat-msg-text" data-id="' + msgs.id + '">' + msg + '</div></div></div>')
                } else {
                    $('#Messages_List').prepend('<div class="chat-msg owner"><div class="chat-msg-profile"><div class="chat-msg-date"><span data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></span><span data-seen="' + msgs.seen + '"></span></div></div><div class="chat-msg-content"><div class="chat-msg-text" data-id="' + msgs.id + '">' + msg + '</div></div></div>')
                }
                getDate(document.querySelectorAll('[data-dateid="' + msgs.id + '"]'));
                getSeen(document.querySelectorAll("[data-seen]"));


            }



        }
    });
}

function convertUTCDateToLocalDate(date) {
    return new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes()));
}

function getDate(date_element) {


    if (date_element.length > 1) {

        for (let i = 0; i < date_element.length; i++) {
            let date = date_element[i].getAttribute("data-date").toString().replaceAll(".", "");


            date = convertUTCDateToLocalDate(new Date(date));

            // LocaleDateString
            let LocaleDateString = date.toLocaleDateString();
            let hours = date.getHours() % 12;
            hours = hours ? hours : 12;
            let minutes = date.getMinutes();
            let ampm = date.getHours() >= 12 ? "PM" : "AM";
            var strTime = LocaleDateString + " " + hours + ':' + minutes + ' ' + ampm;

            date_element[i].innerHTML = strTime;
        }
    } else if (document.querySelectorAll("[data-date]").length == 1) {
        let date = date_element[0].getAttribute("data-date");

        date = convertUTCDateToLocalDate(new Date(date));

        // LocaleDateString
        let LocaleDateString = date.toLocaleDateString();
        let hours = date.getHours() % 12;
        hours = hours ? hours : 12;
        let minutes = date.getMinutes();
        let ampm = date.getHours() >= 12 ? "PM" : "AM";
        var strTime = LocaleDateString + " " + hours + ':' + minutes + ' ' + ampm;
        date_element[0].innerHTML = strTime;
    } else {
        let date = date_element[0].getAttribute("data-date");

        date = convertUTCDateToLocalDate(new Date(date));

        // LocaleDateString
        let LocaleDateString = date.toLocaleDateString();
        let hours = date.getHours() % 12;
        hours = hours ? hours : 12;
        let minutes = date.getMinutes();
        let ampm = date.getHours() >= 12 ? "PM" : "AM";
        var strTime = LocaleDateString + " " + hours + ':' + minutes + ' ' + ampm;
        date_element[0].innerHTML = strTime;
    }
}





function countUpFromTime(countFrom, id) {
    countFrom = new Date(convertUTCDateToLocalDate(new Date(countFrom))).getTime();
    var now = new Date(),
        countFrom = new Date(countFrom),
        timeDifference = (now - countFrom);


    var secondsInADay = 60 * 60 * 1000 * 24,
        secondsInAHour = 60 * 60 * 1000;

    days = Math.floor(timeDifference / (secondsInADay) * 1);
    weeks = Math.floor(days / 7);
    hours = Math.floor((timeDifference % (secondsInADay)) / (secondsInAHour) * 1);
    mins = Math.floor(((timeDifference % (secondsInADay)) % (secondsInAHour)) / (60 * 1000) * 1);


    var idEl = document.querySelector("[data-friendid='" + id + "']");

    if (weeks >= 1) {
        idEl.innerHTML = weeks + "w";
    }
    else if (days >= 1) {
        idEl.innerHTML = days + "d";
    } else if (hours >= 1) {
        idEl.innerHTML = hours + "h";
    } else if (mins >= 1) {
        idEl.innerHTML = mins + "m";
    } else if (days < 1, hours < 1, mins < 1) {
        idEl.innerHTML = 1 + "m";
    }

}

function countUpFromFriendAreaMessages(freindid) {
    if (freindid == 'None') {
        date_elements = document.querySelectorAll("[data-friendid]");
        for (let i = 0; i < date_elements.length; i++) {
            let date = date_elements[i].getAttribute("data-dateconv");
            let date_friendid = date_elements[i].getAttribute("data-friendid");

            countUpFromTime(date, date_friendid);
        }
    } else {
        date_elements = document.querySelector("[data-friendid='" + freindid + "']");
        let date = date_elements.getAttribute("data-dateconv");
        countUpFromTime(date, freindid);
    }

}




function getSeen(elements) {

    svg_seen = ' <svg width="16px" fill="#c0c7d2" height="15px" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fit="" preserveAspectRatio="xMidYMid meet" focusable="false"><path d="M18,7 L16.59,5.59 L10.25,11.93 L11.66,13.34 L18,7 Z M22.24,5.59 L11.66,16.17 L7.48,12 L6.07,13.41 L11.66,19 L23.66,7 L22.24,5.59 Z M0.41,13.41 L6,19 L7.41,17.59 L1.83,12 L0.41,13.41 Z"></path></svg>';
    svg_not_seen = ' <svg  width="16px" fill="#c0c7d2" height="15px" viewBox="0 0 24 24" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fit="" preserveAspectRatio="xMidYMid meet" focusable="false"><g stroke="none" stroke-width="1" fill-rule="evenodd"><polygon fill="none" opacity="0" points="2 2 22 2 22 22 2 22"></polygon><polygon points="20.093 4 7.953 16.3652376 3.908 12.2421336 2 14.1855334 7.954 20.25 22 5.94238122"></polygon></g></svg>';

    for (let i = 0; i < elements.length; i++) {

        let seen = elements[i].getAttribute("data-seen");



        if (seen == "true") {
            elements[i].innerHTML = svg_seen;
        } else {
            elements[i].innerHTML = svg_not_seen;
        }

    }
}


window.onload = function () {

    countUpFromFriendAreaMessages('None');

    // Get Messages Date
    getDate(document.querySelectorAll("[data-date]"));


    setInterval(function () {
        getSeen(document.querySelectorAll("[data-seen]"));
        countUpFromFriendAreaMessages('None');
    }, 1000);

    getSeen(document.querySelectorAll("[data-seen]"));





    // Scroll Dwon When Page Load
    $("#chat-area").scrollTop($("#chat-area")[0].scrollHeight);

    // Detct URL in chat-msg-text element
    var msg = document.getElementsByClassName("chat-msg-text");
    for (var i = 0; i < msg.length; i++) {
        msg[i].innerHTML = URLify(msg[i].innerHTML);
    }



}


function goToCurrentUserProfile() {
    var url = "/accounts/profile/" + $('#current_user').text();
    $('head').append('<meta http-equiv="refresh" content="0; url=' + url + '">')
}









































