from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Post)
admin.site.register(Post_Like)
admin.site.register(Post_Comments)
admin.site.register(Post_Favorite)