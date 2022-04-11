from django.urls import path
from .views import *

app_name = "home"

urlpatterns = [

    path('', Home_Page_views, name='homepage'),
    path('search', Search_Page_views, name="search"),

]
