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
    voice_file = models.FileField(upload_to='voice_files/', null=True, blank=True)
    voice_file_duration = models.IntegerField(null=True, blank=True)


    class Meta:
        verbose_name = 'Private Message'
        verbose_name_plural = 'Private Messages'
        ordering = ['id']

    def __str__(self):
        return self.from_user.username + " to " + self.to_user.username + " - " + self.date_utc