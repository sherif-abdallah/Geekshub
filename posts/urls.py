from django.urls import path
from .views import *

app_name = "posts"

urlpatterns = [
        path('create/', Post_create_views, name="create"),
        path('<int:id>', Post_views, name="post"),
        path('delete/<int:id>', Delete_Post_views, name="delete"),
        path('edit/<int:id>', Edit_Post_views, name="edit"),
]