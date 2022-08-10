from email.mime import image
from accounts.models import Profile_picture
from inbox.models import Messages_Inbox
from django.core.paginator import Paginator
import re, random
from django.db.models import  Q
from datetime import datetime, timezone
from django.contrib.auth.models import User



# Create your Packages here.

def Last_Messages_Friend_id(request):
    msgs = Messages_Inbox.objects.filter(Q(to_user_id=request.user.id) | Q(from_user_id=request.user.id)).values('from_user', 'to_user').order_by('-id')
    if msgs[0]['from_user'] != request.user.id:
        last_msg_friend_id = msgs[0]['from_user']
    elif msgs[0]['to_user'] != request.user.id:
        last_msg_friend_id = msgs[0]['to_user']
    else:
        last_msg_friend_id = None
    

    return last_msg_friend_id

def Message_Notification_views(request):
    msg_notification_bar = Messages_Inbox.objects.filter(to_user_id=request.user.id, seen=False)
    msg_notification_bar_len = msg_notification_bar.count()
    return msg_notification_bar_len


def check_email_is_valid(email):  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex, email)):   
        return True
    else:
        return False

# Check If Company Account didnt send to the user message
def check_if_company_account_didnt_send_to_user(request):
    company_account = User.objects.filter(username="Geekshub")


    if company_account.exists():
        messages_inbox = Messages_Inbox.objects.filter(to_user_id=request.user.id, from_user=company_account[0].id)
        if len(messages_inbox) == 0:
            msg = f"Hi { request.user.username }, Welcome to Geekshub. Your account has been created – now it will be easier than ever to share and connect with your friends and family. Your new account comes with access to Geekshub products, apps, and services."
            Messages_Inbox.objects.create(to_user_id=request.user.id, from_user_id=company_account[0].id, date_utc=datetime.now(timezone.utc).strftime("%Y-%m-%d %I:%M:%S %p"), msg=msg)
    else:
        # Create Company Account
        new_company_account = User.objects.create(username="Geekshub", password="Geekshub@123", email="office@geekshub.com")
        # Create Profile Picture
        Profile_picture.objects.create(author_id=new_company_account.id)
        # Create Message
        messages_inbox = Messages_Inbox.objects.filter(to_user_id=request.user.id, from_user=new_company_account.id)
        if len(messages_inbox) == 0:
            msg = f"Hi { request.user.username }, Welcome to Geekshub. Your account has been created – now it will be easier than ever to share and connect with your friends and family. Your new account comes with access to Geekshub products, apps, and services."
            Messages_Inbox.objects.create(to_user_id=request.user.id, from_user_id=new_company_account.id, date_utc=datetime.now(timezone.utc).strftime("%Y-%m-%d %I:%M:%S %p"), msg=msg)

# Cheek if user dosent have profile picture
def cheek_user_picture(request):
    profile_picture = Profile_picture.objects.filter(author_id=request.user)
    if len(profile_picture) == 0:
        Profile_picture.objects.create(author_id=request.user.id)

# Paginate the posts
def paginate(request, posts, num_posts):
    paginator = Paginator(posts, num_posts)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return posts

# Reverse the list
def Reverse(lst):
    return [ele for ele in reversed(lst)]

# Convert list to string
def listToStringWithoutBrackets(lst):
    return str(lst).replace('[','').replace(']','')



