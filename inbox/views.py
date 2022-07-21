from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from accounts.models import *
from notifications.models import *
from .models import *
from social.defMain import *
from datetime import datetime, timezone


# Create your views here.
@login_required(login_url='accounts:loginuser')
def Inbox_page_views(request, current_userid):


    cheek_user_picture(request)
    check_if_company_account_didnt_send_to_user(request)


    msg_obj = Messages_Inbox.objects
    msg_obj.filter(from_user_id=current_userid, to_user_id=request.user.id, seen=False).update(seen=True)
    msg_obj.filter(to_user_id=request.user.id, seen_home=False).update(seen_home=True)
    
    # Friends Area
    friends = Follow.objects.filter(follower_id=request.user.id).values_list('following_id', flat=True)

    friends_profile_picture = Profile_picture.objects.filter(author_id__in=list(friends))

    # Last Message From Friends
    last_messages = []  

    # Not Friends Area
    not_friends = Messages_Inbox.objects.exclude(Q(from_user_id__in=list(friends), to_user_id=request.user.id) | Q(from_user_id=request.user.id ,to_user_id__in=list(friends))).filter(Q(from_user_id=request.user.id) | Q(to_user_id=request.user.id))
    not_friends_id = []
    for z in not_friends:
        if z.from_user_id == request.user.id:
            not_friends_id.append(z.to_user_id)
        else:
            not_friends_id.append(z.from_user_id)

    not_friends_id = set(not_friends_id)
    
    not_friends_profile_picture = Profile_picture.objects.filter(author_id__in=not_friends_id)

    chats = friends_profile_picture.union(not_friends_profile_picture)


    friends_name = User.objects.filter(id__in=list(friends) + list(not_friends_id))
    friends_name = paginate(request, posts=friends_name, num_posts=10)



    for i in chats:
        x = Messages_Inbox.objects.filter(Q(from_user_id=i.author_id, to_user_id=request.user.id) | Q(from_user_id=request.user.id, to_user_id=i.author_id)).values('msg','from_user', 'to_user', 'date_utc', 'created_at', 'seen').order_by('-id').first()
        if x == None:
            x = {'msg': '', 'from_user': i.author_id, 'to_user': request.user.id, 'date_utc': '', "friend_id": i.author_id, "friend_name": i.author.username, "friend_profile_picture": i.image.url, "created_at": '2005-10-18 12:00:00', "seen": ''}
        else:
            x['friend_id'] = i.author_id
            x['friend_name'] = i.author.username
            x['friend_profile_picture'] = i.image.url
            
            created_at = str(x['created_at'])
            x['created_at'] = created_at[ 0 : created_at.index(".")]

        last_messages.append(x)



    last_messages = sorted(
        list(last_messages),
        key=lambda i: datetime.strptime(i['created_at'], '%Y-%m-%d %H:%M:%S'), reverse=True
    )

    last_messages = paginate(request, posts=last_messages, num_posts=10)


    # ---------------------------------------------------------------------------------------------#

    # Chat Area
    friend_chat_user = User.objects.get(id=int(current_userid))

    friend_chat_user = Profile_picture.objects.get(author_id=friend_chat_user.id)
    print(friend_chat_user)
    # Get all the messages between the current user and the friend
    msgs = Messages_Inbox.objects.filter(Q(from_user_id=friend_chat_user.author_id, to_user_id=request.user.id) | Q(from_user_id=request.user.id, to_user_id=friend_chat_user.author_id)).values('msg','from_user', 'id', 'date_utc', 'seen').order_by('-id')
    msgs_paginate = paginate(request, posts=msgs, num_posts=6)
    msgs = Reverse(msgs_paginate)


    # Home Based on the user's Inbox
    #notification_bar
    notification_bar = Notifications.objects.filter(user=request.user.id, is_seen=False)
    notification_bar_len = len(notification_bar)
    if notification_bar_len == 0:
        bell = False
    else:
        bell = True
    
    # Theme
    theme = Profile_picture.objects.get(author_id=request.user.id).theme
    profile_image = Profile_picture.objects.get(author_id=request.user.id).image.url


    context = {
        # Home Base
        "profile_image": profile_image,
        "theme": theme,
        "bell": bell,
        "notification_bar_len": notification_bar_len, 
        # Friends Area
        "friends_name":friends_name,
        # Chat Area
        "friend_chat_user": friend_chat_user,
        "current_userid": current_userid,
        "last_messages": last_messages,

        "msgs":msgs,
        "msgs_paginate":msgs_paginate,
        "last_msg_friend_id":Last_Messages_Friend_id(request),
        "message_notification_len": Message_Notification_views(request),

    }



    return render(request, 'inbox_page.html', context)


@login_required(login_url='accounts:loginuser')
def Inbox_Messages_API_views(request, current_userid):

    # Get all the messages between the current user and the friend

    msgs = Messages_Inbox.objects.filter(Q(from_user_id=current_userid, to_user_id=request.user.id) | Q(from_user_id=request.user.id, to_user_id=current_userid)).values('msg','from_user', 'id', 'date_utc', 'seen').order_by('-id')
    msgs_paginate = paginate(request, posts=msgs, num_posts=6)
    # msgs = Reverse(msgs_paginate)


    if msgs_paginate.has_next():
        next_page = msgs_paginate.next_page_number()
        has_next = True
    else:
        next_page = None
        has_next = False

    
    return JsonResponse({"msgs": list(msgs_paginate), "paginate": {"next_page": next_page, "has_next": has_next}})



@login_required(login_url='accounts:loginuser')
def Inbox_Messages_API_Lunch_views(request, current_userid):

    # Get all the messages between the current user and the friend
    Messages_Inbox.objects.filter(from_user_id=current_userid, to_user_id=request.user.id, seen=False).update(seen=True)


    msgs = Messages_Inbox.objects.filter(Q(from_user_id=current_userid, to_user_id=request.user.id) | Q(from_user_id=request.user.id, to_user_id=current_userid)).values('msg','from_user', 'id', 'date_utc', 'seen').order_by('-id')
    msgs_paginate = paginate(request, posts=msgs, num_posts=6)
    current_username = User.objects.get(id=current_userid)
    current_username_picture = Profile_picture.objects.get(author_id=current_username.id).image.url



    if msgs_paginate.has_next():
        next_page = msgs_paginate.next_page_number()
        has_next = True
    else:
        next_page = None
        has_next = False

    
    return JsonResponse({"msgs": list(msgs_paginate),  "current_username": current_username.username, "current_username_picture":current_username_picture, "paginate": {"next_page": next_page, "has_next": has_next}})




@login_required(login_url='accounts:loginuser')
def Inbox_page_friends_API_views(request):

    # Friends Area
    friends = Follow.objects.filter(follower_id=request.user.id).values_list('following_id', flat=True)


    # Last Message From Friends
    last_messages = []  

    # Not Friends Area
    not_friends = Messages_Inbox.objects.exclude(Q(from_user_id__in=list(friends), to_user_id=request.user.id) | Q(from_user_id=request.user.id ,to_user_id__in=list(friends))).filter(Q(from_user_id=request.user.id) | Q(to_user_id=request.user.id))
    not_friends_id = []
    for z in not_friends:
        if z.from_user_id == request.user.id:
            not_friends_id.append(z.to_user_id)
        else:
            not_friends_id.append(z.from_user_id)

    not_friends_id = set(not_friends_id)
    
    chats = Profile_picture.objects.filter(author_id__in=list(friends) + list(not_friends_id))


    friends_name = User.objects.filter(id__in=list(friends) + list(not_friends_id))
    friends_name = paginate(request, posts=friends_name, num_posts=10)



    for i in chats:
        x = Messages_Inbox.objects.filter(Q(from_user_id=i.author_id, to_user_id=request.user.id) | Q(from_user_id=request.user.id, to_user_id=i.author_id)).values('msg','from_user', 'to_user', 'date_utc', 'created_at').order_by('-id').first()
        if x == None:
            x = {'msg': '', 'from_user': i.author_id, 'to_user': request.user.id, 'date_utc': '', "friend_id": i.author_id, "friend_name": i.author.username, "friend_profile_picture": i.image.url, "created_at": '2005-10-18 12:00:00'}
        else:
            x['friend_id'] = i.author_id
            x['friend_name'] = i.author.username
            x['friend_profile_picture'] = i.image.url
            
            created_at = str(x['created_at'])
            x['created_at'] = created_at[ 0 : created_at.index(".")]

        last_messages.append(x)



    last_messages = sorted(
        list(last_messages),
        key=lambda i: datetime.strptime(i['created_at'], '%Y-%m-%d %H:%M:%S'), reverse=True
    )

    last_messages = paginate(request, posts=last_messages, num_posts=10)


    
    if last_messages.has_next():
        next_page = friends_name.next_page_number()
        has_next = True
    else:
        next_page = None
        has_next = False


    print(list(last_messages))

                                  
    return JsonResponse({"friends_name": list(last_messages)})


@login_required(login_url='accounts:loginuser')
def CreateMsg_api_views(request):

    msgs_obj = Messages_Inbox.objects

    if request.method == "POST":
       if len(request.POST.get('msg')) != 0:
            create_msgs_obj = msgs_obj.create(from_user_id = request.user.id, to_user_id = request.POST.get('to_user_id'), msg = request.POST.get('msg'), date_utc=datetime.now(timezone.utc).strftime("%Y-%m-%d %I:%M:%S %p"))
            msg = msgs_obj.get(id=create_msgs_obj.id)
            msg_profile_picture = Profile_picture.objects.get(author_id=msg.to_user.id).image.url
            
            new_msg = {"msg": msg.msg, "id": msg.id, "from_user": msg.from_user.username, "date_utc": msg.date_utc, "from_user_id": msg.from_user.id, "to_user_id": msg.to_user.id, "created_at": msg.created_at, "friend_id": msg.to_user.id, "friend_name": msg.to_user.username, "friend_profile_picture": msg_profile_picture, 'seen': msg.seen}
            
            return JsonResponse({"new_msg": new_msg})


@login_required(login_url='accounts:loginuser')
def CheckThereMessage_API_views(request, current_userid):

    new_msg = Messages_Inbox.objects.filter(from_user_id=current_userid, to_user_id=request.user.id, seen=False).values('msg','from_user', 'id', 'date_utc', 'seen').order_by('-id')

    if len(new_msg) == 0: 
        return JsonResponse({"success": False})
    else:
        Messages_Inbox.objects.filter(from_user_id=current_userid, to_user_id=request.user.id, seen=False).update(seen=True)

        return JsonResponse({"success": True, "new_msg": list(new_msg)})



@login_required(login_url='accounts:loginuser')
def CheckThereMessageFromFreinds_API_views(request):

    # Friends Area
    friends = Follow.objects.filter(follower_id=request.user.id).values_list('following_id', flat=True)


    # Not Friends Area
    not_friends = Messages_Inbox.objects.exclude(Q(from_user_id__in=list(friends), to_user_id=request.user.id) | Q(from_user_id=request.user.id ,to_user_id__in=list(friends))).filter(Q(from_user_id=request.user.id) | Q(to_user_id=request.user.id))
    not_friends_id = []
    for z in not_friends:
        if z.from_user_id == request.user.id:
            not_friends_id.append(z.to_user_id)
        else:
            not_friends_id.append(z.from_user_id)

    not_friends_id = set(not_friends_id)


    # Friends Id's and Not Friends Id's
    chats = list(friends) + list(not_friends_id)
    new_msg = Messages_Inbox.objects.filter(to_user_id=request.user.id, from_user_id__in=chats, seen_home=False)


    if len(new_msg) == 0: 
        success = False
        msgs = []
    else:
        success = True
        msg_senders_id_lst = new_msg.values_list('from_user_id', flat=True)
        msg_senders_profile_picture = Profile_picture.objects.filter(author_id__in=msg_senders_id_lst)

        msgs = []

        for i in msg_senders_profile_picture:
            x = Messages_Inbox.objects.filter(to_user_id=request.user.id, from_user_id__in=chats, seen_home=False).values('msg','from_user', 'to_user', 'date_utc', 'created_at', 'seen', 'seen_home').order_by('-id').first()
            x['friend_id'] = i.author_id
            x['friend_name'] = i.author.username
            x['friend_profile_picture'] = i.image.url
                

            msgs.append(x)

        new_msg.update(seen_home=True)
        
        
    return JsonResponse({"success": success, "new_msg": list(msgs)})


@login_required(login_url='accounts:loginuser')
def Message_Notification_API_views(request):
    msg_notification_bar = Messages_Inbox.objects.filter(to_user_id=request.user.id, seen=False)
    msg_notification_bar_len = msg_notification_bar.count()

    return JsonResponse({"msg_notification_bar_len": msg_notification_bar_len})




@login_required(login_url='accounts:loginuser')
def Check_If_Friend_Seen_API_views(request, current_userid):
    
    seen = Messages_Inbox.objects.filter(from_user=request.user.id, to_user=current_userid).values_list('seen').order_by('-id').first()
    
    return JsonResponse({"seen": seen[0]})





@login_required(login_url='accounts:loginuser')
def Main_Inbox_page_views(request):
    pass



