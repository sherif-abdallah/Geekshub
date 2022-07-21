from django.urls import path
from .views import *

app_name = "inbox"

urlpatterns = [
    path('<int:current_userid>/', Inbox_page_views, name='inboxpage'),
    path('messages_api/<int:current_userid>/', Inbox_Messages_API_views, name='messages_api'),
    path('messages_api_lunch/<int:current_userid>/', Inbox_Messages_API_Lunch_views, name='friends_Lunch_api'),
    path('friends_api/', Inbox_page_friends_API_views, name='friends_api'),
    path('check_there_message_from_friends_api/', CheckThereMessageFromFreinds_API_views, name="check_there_message_from_friends_api"),
    
    # Message_Notification_API_views
    path('message_notification_api/', Message_Notification_API_views, name='message_notification_api'),

    # Create a new message Api
    path('create/msg_api/', CreateMsg_api_views, name='create_msg_api'),
    path("check_there_message_api/<int:current_userid>/", CheckThereMessage_API_views, name='check_there_message_api'),

    # Check_If_Friend_Seen_API_views
    path('check_if_friend_seen_api/<int:current_userid>/', Check_If_Friend_Seen_API_views, name='check_if_friend_seen_api'),


    # Main Pages Emtgy 
    path('messages_api', Main_Inbox_page_views, name='messages_home_api'),
    path('messages_api_lunch', Main_Inbox_page_views, name='friends_Lunch_Home_api'),
    path("check_there_message_api", Main_Inbox_page_views, name='check_there_message_home_api'),
    path("check_if_friend_seen_api", Main_Inbox_page_views, name='check_if_friend_seen_home_api'),
    path('', Main_Inbox_page_views, name='Main_inboxpage'),
]