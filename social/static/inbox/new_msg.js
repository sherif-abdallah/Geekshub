// Ajax Method To Load More Messages
$(document).on('submit', '#form_new_msg', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: create_msg_api,
        data:
        {
            msg: $("#msg_input").val(),
            to_user_id: $("#current_user").text(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (Msg, friendJson) {
            $("#msg_input").val("");
            if ($("#msg_input").val() == '') {
                Msg = Msg.new_msg;
                if (Msg.to_user_id == $("#current_user").text() && Msg.from_user_id == request_user_id) {

                    if (isHTML(Msg.msg) == false) {
                        msg = URLify(Msg.msg);
                    } else {
                        msg = Msg.msg;
                    }

                    $('#Messages_List').append('<div class="chat-msg owner"><div class="chat-msg-profile"><div class="chat-msg-date"><span data-dateid="' + Msg.id + '" data-date=" ' + Msg.date_utc + '"></span><span data-seen="' + Msg.seen + '"></span></div></div><div class="chat-msg-content"><div class="chat-msg-text" data-id="' + Msg.id + '">' + msg + '</div></div></div>');
                    
                    
                    getDate(document.querySelectorAll('[data-dateid="' + Msg.id +'"]'));
                    getSeen(document.querySelectorAll("[data-seen]"));

                    // Scroll Dwon When Page Loads
                    $('#chat-area').animate({scrollTop: $('#chat-area').prop("scrollHeight")}, 500);


                    // Add New Message To Conversation Area and Freind Area
                    element = document.querySelector('[data-freinduserid="' + Msg.friend_id + '"]');
                    if (element != null) {
                        element.remove();
                    }

                    if (Msg.msg.length != 0) {
                        $('a[data-freindUserid="' + Msg.friend_id + '"]');
                        $('#conversation-area-js').prepend('<a onclick="reloadChatArea(' + Msg.friend_id + ')" id="conversation-area-friend-Link" data-freindUserid="' + Msg.friend_id + '"><div class="msg" $("#chat-area").scrollTop($("#chat-area").height()); data-userid="' + Msg.friend_id + '"><img class="msg-profile" src="' + Msg.friend_profile_picture + '" alt=""><div class="msg-detail"><div class="msg-username">' + Msg.friend_name + '</div><div class="msg-content"><span class="msg-message">' + Msg.msg + '</span><span class="msg-date" data-friendid="' + Msg.friend_id + '" data-dateconv="' + Msg.date_utc + '"></span></div></div></div></a>');
                        countUpFromFriendAreaMessages(Msg.friend_id)
                    } else {
                        $('#conversation-area-js').prepend('<a onclick="reloadChatArea(' + Msg.friend_id + ')" id="conversation-area-friend-Link" data-freindUserid="' + Msg.friend_id + '"><div class="msg" $("#chat-area").scrollTop($("#chat-area").height()); data-userid="' + Msg.friend_id + '"><img class="msg-profile" src="' + Msg.friend_profile_picture + '" alt=""><div class="msg-detail"><div class="msg-username">' + Msg.friend_name + '</div><div class="msg-content"></div></div></div></a>');
                    }

                    let msg_elment =  document.querySelector('[data-userid="' + Msg.friend_id + '"]')

                    if ($("#current_user").text() == Msg.friend_id && $(".active").length == 0) {
                        msg_elment.classList.add('active');
                    }
                    if (Msg.seen == false && $('#current_user').text() != Msg.friend_id) {
                        msg_elment.classList.add('online');
                    }


                }
            }
        }
    })

});

// Check If there any New Message
setInterval(function () {
    $.ajax({
        type: 'GET',
        url: check_there_message_home_api + "/" + $("#current_user").text(),
        data: {},
        success: function (new_msgs) {
            if (new_msgs.success == true) {
                for (let i = 0; i < new_msgs.new_msg.length; i++) {

                    let msgs = new_msgs.new_msg[i];
                    let new_msg = msgs.msg;

                    // Make <a href="https://www.google.com"> if thir a link
                    if (isHTML(new_msg) == false) {
                        new_msg = URLify(new_msg);
                    } else {
                        new_msg = new_msg;
                    }

                    $('#Messages_List').append('<div class="chat-msg not-owner"><div class="chat-msg-profile"><div class="chat-msg-date" data-dateid="' + msgs.id + '" data-date=" ' + msgs.date_utc + '"></div></div><div class="chat-msg-content"><div class="chat-msg-text" data-id="' + msgs.id + '">' + new_msg + '</div></div></div>')


                    getDate(document.querySelectorAll('[data-dateid="' + msgs.id +'"]'));
                    // Scroll Dwon When Page Load
                    $('#chat-area').animate({scrollTop: $('#chat-area').prop("scrollHeight")}, 500);


                }
            }
        }
    })
}, 500);