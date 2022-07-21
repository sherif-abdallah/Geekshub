from django.db import models

# Create your models here.
class Messages_Inbox(models.Model):
    from_user = models.ForeignKey('auth.User', related_name='msgFromUser', on_delete=models.CASCADE)
    to_user = models.ForeignKey('auth.User', related_name='msgToUser',on_delete=models.CASCADE)
    date_utc = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    msg = models.TextField(max_length=1000, null=True,blank=True)
    seen = models.BooleanField(default=False)
    seen_home = models.BooleanField(default=False)

    def __str__(self):
        return "From: " + str(self.from_user.id) + " - To: " + str(self.to_user.id) + " - Message: " + str(self.msg)
    class Meta:
        verbose_name_plural = "Private Messages"