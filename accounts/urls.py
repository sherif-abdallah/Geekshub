from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from posts.models import *

app_name = "accounts"

urlpatterns = [

    path('login/', LoginView.as_view(template_name='login.html'), name='loginuser'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name="logoutuser"),
    path('signup/', register, name="signup"),

    path('profile/<int:userid>', Profile_views, name="profile"),

    path('profile/edit', Edit_Profile_views, name="editprofile"),
    
]

