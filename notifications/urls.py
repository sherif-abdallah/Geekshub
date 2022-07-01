from django.urls import path
from .views import *

app_name = "notifications"

urlpatterns = [
        path('', Notification_Page_views , name="inbox"),
        path('json/', Notification_Json_Api_Views , name="json"),
]