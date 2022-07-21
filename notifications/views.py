from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import *
from .models import *
from social.defMain import *


# Create your views here.
@login_required(login_url='accounts:loginuser')
def Notification_Page_views(request):
    cheek_user_picture(request)
    check_if_company_account_didnt_send_to_user(request)

    # Seen All The Notigication when open the page
    Notifications.objects.filter(user=request.user.id, is_seen=False).update(is_seen=True)

    # Cheek if there notification
    cheek_notification = len(Notifications.objects.filter(user=request.user.id))
    
    # Suggestions For You
    suggestions = Follow.objects.values_list('following').annotate(most=Count('following')).order_by('-most')[:3]
    suggestions_id = [a_tuple[0] for a_tuple in suggestions]
    suggestions_data = User.objects.all()
    suggestions_image = Profile_picture.objects.all()

    # notification page
    notifications = Notifications.objects.filter(user_id=request.user)
    notifications = Reverse(notifications)
    notifications = paginate(request, notifications, 7)
    notifyers_image = Profile_picture.objects.all()


    #notification_bar
    notification_bar = Notifications.objects.filter(user=request.user.id, is_seen=False)
    notification_bar_len = len(notification_bar)
    if notification_bar_len == 0:
        bell = False
    else:
        bell = True

    context = {
        "profile_image": Profile_picture.objects.get(author_id=request.user.id).image.url,
        "suggestions_id":suggestions_id,
        "suggestions_data":suggestions_data,
        "suggestions_image":suggestions_image,
        "cheek_notification":cheek_notification,
        "notifications":notifications,
        "notifyers_image":notifyers_image,
        "notification_bar_len":notification_bar_len,
        "bell":bell,
        "theme":Profile_picture.objects.get(author_id=request.user.id).theme,
        "last_msg_friend_id":Last_Messages_Friend_id(request),
        "message_notification_len": Message_Notification_views(request),

    }
    return render(request, 'notification.html', context)

def Notification_json_api(request):
    notifications = Notifications.objects.filter(user_id=request.user.id, is_seen=False).count()

    return JsonResponse({"notifications":notifications})