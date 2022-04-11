from django.urls import path, reverse
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from posts.models import *

app_name = "accounts"

urlpatterns = [
    # Login or Sign up
    path('user/login/', LoginView.as_view(template_name='login.html'), name='loginuser'),
    path('user/logout/', LogoutView.as_view(template_name='logout.html'), name="logoutuser"),

    path('user/signup/', register, name="signup"),
    # Profile
    path('profile/<int:userid>', Profile_views, name="profile"),
    path('profile/edit', Edit_Profile_views, name="editprofile"),


]