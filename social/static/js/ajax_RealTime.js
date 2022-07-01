$('document').ready(function () {
    setInterval(function () {getRealData()}, 1000);
    }); 
   
   function getRealData() {
   $.ajax({
            url: jsonNotificationURL,
            type: "GET",
            data: {},
            cache: false,
            success: function (notification_bar_len) {
                var notification_bar_len = notification_bar_len['notification_bar_len']
                elementInbox = document.getElementById('notifications-inbox');
                // elementInbox.style = "display: block; padding-left: 1000px;";
                elementInbox.innerHTML = notification_bar_len;


                if(notification_bar_len > 99) {
                    elementInbox.style = "display: inline-block; font-size: 12px; padding: 2px; padding-left: 3px;";
                    elementInbox.innerHTML = 99;
                }
                else if(notification_bar_len > 9 && notification_bar_len <= 99) {
                    elementInbox.style = "display: inline-block; font-size: 12px; padding: 2px; padding-left: 3px;";
                    elementInbox.innerHTML = notification_bar_len;
                }
                else if(notification_bar_len == 0){
                    elementInbox.style = "display: none;"
                }
                 else {
                    elementInbox.removeAttribute("style");
                    elementInbox.style = "display: inline-block; padding-left: 5.2px;";
                }
                
            }
        });
}
