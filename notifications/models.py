
from django.db import models
from django.contrib.auth.models import User
from posts.models import *

# Create your models here.
NOTIFICATION_TYPES = (
    (1,'Like'),
    (2,'Comment'),
    (3,'Follow'))

class Notifications(models.Model):

	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="noti_post", blank=True, null=True)
	comment = models.ForeignKey(Post_Comments, on_delete=models.CASCADE, related_name="noti_comment", blank=True, null=True)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user")
	notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
	text_preview = models.CharField(max_length=90, blank=True)
	date = models.CharField(max_length=10000)
	is_seen = models.BooleanField(default=False)