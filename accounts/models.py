from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

THEME_CHOICE = (
    ('Light Mode', 'Light Mode'),
    ('Dark Mode', 'Dark Mode'),
)

# Create your models here.
class Profile_picture(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE , null=False, blank=False)
    image = models.ImageField(upload_to="", default='posts/default.jpg')
    theme = models.CharField(max_length=1000, choices=THEME_CHOICE, default='Light Mode')

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     # if img.height > 300 or img.width > 100 :
    #     output_size = (400, 400)
    #     img.thumbnail(output_size)
    #     img.save(self.image.path)

class Follow(models.Model):
    follower = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="following")
    def __str__(self):
        return str(self.follower) + " - Following - " + str(self.following)
