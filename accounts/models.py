from PIL import Image
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models import Count


# Create your models here.
THEME_CHOICE = (
    ('Light Mode', 'Light Mode'),
    ('Dark Mode', 'Dark Mode'),
)
class Profile_picture(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE , null=False, blank=False)
    image = models.ImageField(upload_to="", default='posts/default.jpg')
    theme = models.CharField(max_length=1000, choices=THEME_CHOICE, default='Light Mode')
    class Meta:
        verbose_name = 'Profile Picture'
        verbose_name_plural = 'Profile Pictures'
        ordering = ['id']
    def __str__(self):
        return self.author.username + " Profile Picture" + " - " + self.theme


class Follow(models.Model):
    follower = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="following")
    class Meta:
        verbose_name = 'Frined'
        verbose_name_plural = 'Friends'
        ordering = ['id']
    
    def __str__(self):
        return self.follower.username + " is following " + self.following.username