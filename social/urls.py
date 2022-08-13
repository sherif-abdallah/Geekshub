from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from home.views import Redirect_favicon_View
from django.views.static import serve
from django.urls import re_path as url

# Admin site
admin.site.site_header = "Geekshub Admin"
admin.site.site_title = "Geekshub Admin Portal"
admin.site.index_title = "Welcome to Geekshub Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    # allauth
    path('accounts/', include('allauth.urls')),


    path('accounts/', include('accounts.urls'), name="accounts"),
    path('post/', include('posts.urls'), name="posts"),
    path('', include('home.urls'), name="home"),

    # Notifications
    path('notifications/', include('notifications.urls'), name="notifications"),

    # Inbox
    path('messages/', include('inbox.urls'), name="messages"),

    # favicon.ico
    path('favicon.ico', Redirect_favicon_View, name='favicon.ico'),

    # Reset Password
    path('reset_password/', PasswordResetView.as_view(email_template_name="password_reset/password_reset_email.html",html_email_template_name="password_reset/password_html_reset_email.html" , template_name="password_reset/reset_password.html"), name="password_reset"),
    path('reset_password_sent/', PasswordResetDoneView.as_view(template_name="password_reset/reset_sent.html"), name="password_reset_done"),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="password_reset/password_reset_confim.html"), name="password_reset_confirm"),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name="password_reset/password_reset_complete.html"), name="password_reset_complete"),

    # STATIC and MEDIA URLS
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
