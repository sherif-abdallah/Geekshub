from django.contrib import admin
from .models import *

# Register your models here.
class Messages_Inbox_Admin(admin.ModelAdmin):
    readonly_fields = ('date_utc', 'created_at')


admin.site.register(Messages_Inbox, Messages_Inbox_Admin)