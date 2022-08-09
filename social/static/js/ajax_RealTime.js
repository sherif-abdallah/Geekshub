$('.nav-group').ready(function () {
    getRealData();    
    setInterval(function () {getRealData()}, 1000);
}); 

    


function getRealData() {
    // Notification
   $.ajax({
            url: jsonNotificationURL,
            type: "GET",
            data: {},
            cache: false,
            success: function (notification_bar_len) {
                var notification_bar_len = notification_bar_len['notifications']
                elementInbox = document.getElementById('notifications-inbox');
                elementInbox.removeAttribute("style");



                if(notification_bar_len > 99) {
                    elementInbox.style = "display: inline-block; font-size: 11px; padding-right: 3.2px; padding-left: 3.5px; padding-top: 3px; font-wight: bold;";
                    elementInbox.innerHTML = 99;
                }
                else if(notification_bar_len > 9 && notification_bar_len <= 99) {
                    elementInbox.style = "display: inline-block; font-size: 11px; padding-right: 3.2px; padding-left: 3.5px; padding-top: 3px; font-wight: bold;";
                    elementInbox.innerHTML = notification_bar_len;
                }
                else if(notification_bar_len == 0){
                    elementInbox.style = "display: none;"
                }
                 else {
                    elementInbox.style = "display: inline-block; font-size: 12px; padding-right: 3px; padding-left: 6px; padding-top: 2px; font-wight: bold;";
                    elementInbox.innerHTML = notification_bar_len;
                }
                
            }
        });

    // Message Notification
    $.ajax({
        url: msgInboxNotificationURL,
        type: "GET",
        data: {},
        cache: false,
        success: function (msg_notification_bar_len) {
            var msg_notification_bar_len = msg_notification_bar_len['msg_notification_bar_len'];
            elementMsgInbox = document.getElementById('msg-inbox');
            elementMsgInbox.removeAttribute("style");


            if(msg_notification_bar_len > 99) {
                elementMsgInbox.style = "display: inline-block; font-size: 11px; padding-right: 3.2px; padding-left: 3.5px; padding-top: 3px; font-wight: bold;";
                elementMsgInbox.innerHTML = 99;
            }

            else if(msg_notification_bar_len == 0){
                elementMsgInbox.style = "display: none;";
            }
            else if(msg_notification_bar_len > 9 && msg_notification_bar_len <= 99) {
                elementMsgInbox.style = "display: inline-block; font-size: 11px; padding-right: 3.2px; padding-left: 3.5px; padding-top: 3px; font-wight: bold;";
                elementMsgInbox.innerHTML = msg_notification_bar_len;
            }
            else {
                elementMsgInbox.style = "display: inline-block; font-size: 12px; padding-right: 3px; padding-left: 6px; padding-top: 2px; font-wight: bold;";
                elementMsgInbox.innerHTML = msg_notification_bar_len;
            }
            
        }
    });
}