"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('admin/', admin.site.urls),
    # allauth
    path('accounts/', include('allauth.urls')),


    path('accounts/', include('accounts.urls'), name="accounts"),
    path('post/', include('posts.urls'), name="posts"),
    path('', include('home.urls'), name="home"),
    # Notifications
    path('notifications/', include('notifications.urls'), name="notifications"),

    # Reset Password
    path('reset_password/', PasswordResetView.as_view(template_name="password_reset/reset_password.html"), name="password_reset"),
    path('reset_password_sent/', PasswordResetDoneView.as_view(template_name="password_reset/reset_sent.html"), name="password_reset_done"),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="password_reset/password_reset_confim.html"), name="password_reset_confirm"),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name="password_reset/password_reset_complete.html"), name="password_reset_complete"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
