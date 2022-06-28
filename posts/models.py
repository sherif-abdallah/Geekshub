from PIL import Image
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE , null=False, blank=False)
    body = models.TextField()
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    created_on = models.CharField(max_length=10000)
    def __str__(self):
        return str(self.author) + " -> " + str(self.body)


    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     # if img.height > 300 or img.width > 100 :
    #     output_size = (400, 400)
    #     img.thumbnail(output_size)
    #     img.save(self.image.path)

class Post_Like(models.Model):
    liker = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.liker) + " -> " + str(self.post)

class Post_Comments(models.Model):
    commenter = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_body = models.TextField()

    creared_on = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.commenter) + " -> " + str(self.post)