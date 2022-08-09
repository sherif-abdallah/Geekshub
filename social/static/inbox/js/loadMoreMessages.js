$(window).on('load', function () {
    $(".chat-area").scrollTop($(".chat-area")[0].scrollHeight);
});


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
        window.history.pushState("/messages/" + page_id + "/" + "?friends_area=" + friends_area, 'Geekshub', "/messages/" + page_id + "/" + "?friends_area=" + friends_area);


        $.ajax({
            url: friends_Lunch_api + "/" + page_id + "?page=" + 1,
            type: "GET",
            data: {},
            cache: false,
            success: function (MessagesJson) {
                // Stop Recording Audio
                if (voiceRecorder.isRecording) { voiceRecorder.disablerecording(); }
                // Change and Delete Chat Area Content
                $('#loadMoreMessagesButton').hide();
                $('#userpicture').attr('href', "/accounts/profile/" + page_id);
                $('#usertitle').attr('href', "/accounts/profile/" + page_id);
                $(".chat-area-title").html(MessagesJson.current_username);
                $(".chat-area-profile").attr("src", MessagesJson.current_username_picture)
                $("#msg_input").val("")

                if ($('.chat-msg').length != 0) {
                    $(".chat-msg").remove();
                }

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
                            if (msgs.voice_file.length != 0 || msgs.voice_file != '' && msgs.voice_file == voice_message_text) {
                                // if Voice Message is Sent
                                $("#Messages_List").prepend('<div class="chat-msg not-owner" data-msgid="' + msgs.id + '"><div class="chat-msg-profile"><div class="chat-msg-date" data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></div></div><audio class="voicerecord_audio" data-duration="' + msgs.voice_file_duration + '" style="display: block;" preload="auto" controls hidden><source src="/media' + msgs.voice_file + '"></audio></div>');

                                loadAudioDesign('[data-msgid="' + msgs.id + '"] .voicerecord_audio');
                            } else {
                                // if Text Message is Sent
                                $('#Messages_List').prepend('<div class="chat-msg not-owner" data-msgid="' + msgs.id + '"><div class="chat-msg-profile"><div class="chat-msg-date" data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></div></div><div class="chat-msg-content"><div class="chat-msg-text" data-id="' + msgs.id + '">' + msg + '</div></div></div>')
                            }
                        } else {
                            if (msgs.voice_file.length != 0 || msgs.voice_file != '' && msgs.voice_file == voice_message_text) {
                                $('#Messages_List').prepend('<div class="chat-msg owner" data-msgid="' + msgs.id + '"><div class="chat-msg-profile"><div class="chat-msg-date"><span data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></span><span data-seen="' + msgs.seen + '"></span></div></div><audio class="voicerecord_audio" data-duration="' + msgs.voice_file_duration + '" style="display: block;" preload="auto" controls hidden><source src="/media' + msgs.voice_file + '"></audio></div>')

                                loadAudioDesign('[data-msgid="' + msgs.id + '"] .voicerecord_audio');
                            } else {
                                $('#Messages_List').prepend('<div class="chat-msg owner" data-msgid="' + msgs.id + '"><div class="chat-msg-profile"><div class="chat-msg-date"><span data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></span><span data-seen="' + msgs.seen + '"></span></div></div><div class="chat-msg-content"><div class="chat-msg-text" data-id="' + msgs.id + '">' + msg + '</div></div></div>')
                            }
                        }

                        getDate(document.querySelectorAll('[data-dateid="' + msgs.id + '"]'));
                        getSeen(document.querySelectorAll("[data-seen]"));


                        document.querySelector('[data-userid="' + page_id + '"]').classList.remove("online");


                    }
                    
                }


                try {
                    active_element = document.getElementsByClassName("msg active");

                    for (let i = 0; i < active_element.length; i++) {
                        active_element[i].classList.remove("active");
                    }
                } catch (error) {

                }
                document.querySelector('[data-userid="' + page_id + '"]').classList.add('active');
                $("#current_user").text(page_id);

                // Onlick in msg frinds diplay none for firends area and show for chat area

                function ifMobile(ismobile) {
                    if (ismobile.matches) {
                        $('.conversation-area').css({ 'display': 'none' });
                        $('.chat-area').show();
                        $('#header').css({ 'display': 'none' });
                        $(".breakLine_br").css({ 'display': 'none' });
                        $(".chat-area-header").css({ "padding": "15px" });
                        $(".chat-area-profile").css({ "margin-bottom": "6px" });
                        $(".chat-area-title").css({ "margin-bottom": "6px" });
                        $('.app').css({ 'height': '100vh' });
                    }
                }

                // If User is Mobile
                var ismobile = window.matchMedia("(max-width: 700px)")
                ifMobile(ismobile) // Call listener function at run time
                ismobile.addListener(ifMobile) // Attach listener function on state changes


            }
            
        }).done(function (data) {
            $(".chat-area").scrollTop($(".chat-area")[0].scrollHeight);
        });



    }
}


var msgs_paginate = 2;
// Ajax Method To Load More Messages
function loadMoreMessagesButton() {
    $('#loadMoreMessagesButton').hide();
    $.ajax({
        url: $("#messages_home_api").text() + "/" + $("#current_user").text() + "?page=" + msgs_paginate,
        type: "GET",
        data: {},
        cache: false,
        success: function (MessagesJson) {

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

                /*
                */


                if (from_user != request_user_id) {

                    if (msgs.voice_file.length != 0 || msgs.voice_file != '' && msgs.msg == voice_message_text) {
                        // If Voice Message is Sent
                        $('#Messages_List').prepend('<div class="chat-msg not-owner" data-msgid="' + msgs.id + '"><div class="chat-msg-profile"><div class="chat-msg-date" data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></div></div><audio class="voicerecord_audio" data-duration="' + msgs.voice_file_duration + '" style="display: block;" preload="auto" controls hidden><source src="/media' + msgs.voice_file + '"></audio></div>')
                        loadAudioDesign('[data-msgid="' + msgs.id + '"] .voicerecord_audio');
                    } else {
                        // If Text Message is Sent
                        $('#Messages_List').prepend('<div class="chat-msg not-owner" data-msgid="' + msgs.id + '"><div class="chat-msg-profile"><div class="chat-msg-date" data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></div></div><div class="chat-msg-content"><div class="chat-msg-text" data-id="' + msgs.id + '">' + msg + '</div></div></div>')
                    }
                } else {
                    if (msgs.voice_file.length != 0 || msgs.voice_file != '' && msgs.msg == voice_message_text) {
                        // If Voice Message is Sent
                        $('#Messages_List').prepend('<div class="chat-msg owner" data-msgid="' + msgs.id + '"><div class="chat-msg-profile"><div class="chat-msg-date"><span data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></span><span data-seen="' + msgs.seen + '"></span></div></div><audio class="voicerecord_audio" data-duration="' + msgs.voice_file_duration + '" style="display: block;" preload="auto" controls hidden><source src="/media' + msgs.voice_file + '"></audio></div>')

                        loadAudioDesign('[data-msgid="' + msgs.id + '"] .voicerecord_audio');
                    } else {
                        // If Text Message is Sent
                        $('#Messages_List').prepend('<div class="chat-msg owner" data-msgid="' + msgs.id + '"><div class="chat-msg-profile"><div class="chat-msg-date"><span data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></span><span data-seen="' + msgs.seen + '"></span></div></div><div class="chat-msg-content"><div class="chat-msg-text" data-id="' + msgs.id + '">' + msg + '</div></div></div>')
                    }
                }
                getDate(document.querySelectorAll('[data-dateid="' + msgs.id + '"]'));
                getSeen(document.querySelectorAll("[data-seen]"));


            }

            if (MessagesJson.paginate.has_next == true) {
                msgs_paginate = MessagesJson.paginate.next_page;
                $('#loadMoreMessagesButton').show();
            }
            else {
                msgs_paginate = 2;
                $('#loadMoreMessagesButton').hide();
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
    if (theme == "Dark Mode") {
        document.body.classList.add("dark-mode");
    }


    // Check if mobile or desktop device is used and set the correct variables
    function CheckIfMobile(is_mobile) {
        if (is_mobile.matches) {
            if (friends_area == 'true') {
                $('.conversation-area').css({ 'display': 'block', 'width': '100%', 'height': '100%' });
                $('.chat-area').css({ 'display': 'none' });
                $(".breakLine_br").css({ 'display': 'block' });
                // Remove Active Class From Friends Area
                $('.msg.active').removeClass('active');
            } else if (friends_area == 'false') {
                $('.conversation-area').css({ 'display': 'none' });
                $('#header').css({ 'display': 'none' });
                $(".breakLine_br").css({ 'display': 'none' });
                $('.chat-area').show();

                $(".chat-area-header").css({ "padding": "15px" });
                $(".chat-area-profile").css({ "margin-bottom": "6px" });
                $(".chat-area-title").css({ "margin-bottom": "6px" });
                $('.app').css({ 'height': '100vh' });
            }


        } else {
            // Add Active Class To Friends Area if it is not active
            if ($('.msg.active').length == 0) {
                $('[data-userid="' + $("#current_user").text() + '"]').first().addClass('active');
            }
            // Remove Style Attribute From Conversation Area
            $('#header').css({ 'display': 'block' });
            $(".breakLine_br").css({ 'display': 'block' });
            $('.chat-area-header').removeAttr('style');
            $('.chat-area-profile').removeAttr('style');
            $('.chat-area-title').removeAttr('style');
            $('.app').removeAttr('style');
            $('.chat-area').show();
            $('.conversation-area').css({ 'display': 'block', 'width': '340px' });
        }
    }


    var is_mobile = window.matchMedia("(max-width: 700px)")
    CheckIfMobile(is_mobile) // Call listener function at run time
    is_mobile.addListener(CheckIfMobile) // Attach listener function on state changes

    
    loadAudioDesign('.voicerecord_audio');
    const voice_message_text = "sent a voice message";
    $(".chat-area").scrollTop($(".chat-area")[0].scrollHeight);








    $('#userpicture').attr('href', "/accounts/profile/" + $('#current_user').text());
    $('#usertitle').attr('href', "/accounts/profile/" + $('#current_user').text());

    countUpFromFriendAreaMessages('None');

    // Get Messages Date
    try {
        getDate(document.querySelectorAll("[data-date]"));
    } catch (error) {
    }


    setInterval(function () {
        getSeen(document.querySelectorAll("[data-seen]"));
        countUpFromFriendAreaMessages('None');
    }, 1000);

    getSeen(document.querySelectorAll("[data-seen]"));


    // Detct URL in chat-msg-text element
    var msg = document.getElementsByClassName("chat-msg-text");
    for (var i = 0; i < msg.length; i++) {
        msg[i].innerHTML = URLify(msg[i].innerHTML);
    }

    function moveButton_Match(matches) {
        if (matches.matches) { // If media query matches
            move_display = "none";
        } else {
            move_display = "block";
        }
    }

    var matches = window.matchMedia("(max-width: 700px)")
    moveButton_Match(matches) // Call listener function at run time
    matches.addListener(moveButton_Match) // Attach listener function on state changes

}
