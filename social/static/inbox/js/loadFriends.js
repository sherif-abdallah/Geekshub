function loadAudioDesign(element) {

    $(element).audioPlayer();


    let elements = $(element);
    for (let i = 0; i < elements.length; i++) {
        const element = elements[i];
        // Get Attr Duration
        let duration = element.getAttribute('data-duration');
        // Get Msgid
        let msgid = $(element).parent().parent().attr("data-msgid");

        // Get Message element by msgid
        let msg_element = $('[data-msgid="' + msgid + '"] .audioplayer-time-current');

        // Set Duration
        if (duration <= 9) {
            msg_element.text("00:0" + duration);
        } else if (duration >= 10) {
            msg_element.text("00:" + duration);
        } else if (duration >= 60) {
            msg_element.text("01:00");
        } else {
            msg_element.text("00:00");
        }

        
    }
}

// Ajax Method To Load More Friends
$('#loadMoreFriendsButton').click(function () {
    $('#loadMoreFriendsButton').hide();
    $.ajax({

        url: loadMoreFriends_URL + "?page=" + next_page_friends,
        type: "GET",
        data: {},
        cache: false,
        success: function (friendsJson) {

            for (let friend = 0; friend < friendsJson.friends_name.length; friend++, last_message = friendsJson.last_messages) {
                let friend_name = friendsJson.friends_name[friend];
                let friends_profile_picture = friendsJson.friends_name[friend];

                if (friend_name.msg.length != 0) {
                    $('#conversation-area-js').append('<a onclick="reloadChatArea(' + friend_name.friend_id + ')" id="conversation-area-friend-Link" data-freindUserid="' + friend_name.friend_id + '"><div class="msg"   data-userid="' + friend_name.friend_id + '"><img class="msg-profile" src="' + friends_profile_picture.friend_profile_picture + '" alt=""><div class="msg-detail"><div class="msg-username">' + friend_name.friend_name + '</div><div class="msg-content"><span class="msg-message">' + friend_name.msg + '</span><span class="msg-date" data-friendid="' + friend_name.friend_id + '" data-dateconv="' + friend_name.date_utc + '"></span></div></div></div></a>');
                    countUpFromFriendAreaMessages(friend_name.friend_id)
                } else {
                    $('#conversation-area-js').append('<a onclick="reloadChatArea(' + friend_name.friend_id + ')" id="conversation-area-friend-Link" data-freindUserid="' + friend_name.friend_id + '"><div class="msg"   data-userid="' + friend_name.friend_id + '"><img class="msg-profile" src="' + friends_profile_picture.friend_profile_picture + '" alt=""><div class="msg-detail"><div class="msg-username">' + friend_name.friend_name + '</div><div class="msg-content"></div></div></div></a>');
                }

                if ($("#current_user").text() == friend_name.friend_id && $(".active").length == 0) {
                    document.querySelector('[data-userid="' + friend_name.friend_id + '"]').classList.add('active');
                }

            }
            if (friendsJson.has_next == true) {
                next_page_friends = friendsJson.next_page;
                $('#loadMoreFriendsButton').show();
            } else {
                next_page_friends = null;
                $('#loadMoreFriendsButton').hide();
            }
        }
    });
});

setInterval(function () {
    $.ajax({

        url: check_there_message_from_friends_api,
        type: "GET",
        data: {},
        cache: false,
        success: function (friendsJson) {

            if (friendsJson.success == true) {

                for (let friend = 0; friend < friendsJson.new_msg.length; friend++) {
                    let friend_name = friendsJson.new_msg[friend];
                    let friends_profile_picture = friendsJson.new_msg[friend];


                    if (friend_name.seen == false && $('#current_user').text() != friend_name.friend_id && friend_name.seen_home == false) {
                        let audio = new Audio(message_tune)
                        audio.play();
                    }

                    element = document.querySelector('[data-freinduserid="' + friend_name.friend_id + '"]');
                    if (element != null) {
                        element.remove();
                    }


                    if (friend_name.msg.length != 0) {
                        $('a[data-freindUserid="' + friend_name.friend_id + '"]');
                        $('#conversation-area-js').prepend('<a onclick="reloadChatArea(' + friend_name.friend_id + ')" id="conversation-area-friend-Link" data-freindUserid="' + friend_name.friend_id + '"><div class="msg"   data-userid="' + friend_name.friend_id + '"><img class="msg-profile" src="' + friends_profile_picture.friend_profile_picture + '" alt=""><div class="msg-detail"><div class="msg-username">' + friend_name.friend_name + '</div><div class="msg-content"><span class="msg-message">' + friend_name.msg + '</span><span class="msg-date" data-friendid="' + friend_name.friend_id + '" data-dateconv="' + friend_name.date_utc + '"></span></div></div></div></a>');
                        countUpFromFriendAreaMessages(friend_name.friend_id)
                    } else {
                        $('#conversation-area-js').prepend('<a onclick="reloadChatArea(' + friend_name.friend_id + ')" id="conversation-area-friend-Link" data-freindUserid="' + friend_name.friend_id + '"><div class="msg"   data-userid="' + friend_name.friend_id + '"><img class="msg-profile" src="' + friends_profile_picture.friend_profile_picture + '" alt=""><div class="msg-detail"><div class="msg-username">' + friend_name.friend_name + '</div><div class="msg-content"></div></div></div></a>');
                    }

                    let msg_elment = document.querySelector('[data-userid="' + friend_name.friend_id + '"]')

                    if ($("#current_user").text() == friend_name.friend_id && $(".active").length == 0) {
                        msg_elment.classList.add('active');
                    }
                    if (friend_name.seen == false && $('#current_user').text() != friend_name.friend_id) {
                        msg_elment.classList.add('online');
                    }



                }
            }

        }
    });
}, 1000);


// Onclick exitChatArea icon to exit chat area and go back to home page
$('#exitChatArea').click(function () {
    if (voiceRecorder.isRecording) { voiceRecorder.disablerecording(); }

    $('.chat-area').css('display', 'none');
    $('.conversation-area').css({ 'display': 'block' });
    $('#header').css({ 'display': 'block' });
    $(".breakLine_br").css({ 'display': 'block' });
    // Remove Active Class From Friends Area
    $('.msg.active').removeClass('active');

    $(".chat-area-header").removeAttr('style');
    $(".chat-area-profile").removeAttr('style');
    $(".chat-area-title").removeAttr('style');
    $('.app').removeAttr('style');
});
