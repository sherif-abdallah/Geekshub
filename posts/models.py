from django.db import models

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE , null=False, blank=False)
    body = models.TextField()
    image = models.ImageField(upload_to="posts/", null=True, blank=True)#let's work now with image but will will update this later
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['id']
    
    def __str__(self):
        return self.author.username + " - " + self.created_on

class Post_Like(models.Model):
    liker = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_date=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        ordering = ['id']

    def __str__(self):
        if self.liker == self.post.author:
            return self.liker.username + " liked his own post"
        else:
            return self.liker.username + " liked " + self.post.author.username + "'s post"

class Post_Comments(models.Model):
    commenter = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_body = models.TextField()
    #dates
    comment_date = models.DateField(auto_now_add=True)
    edit_date=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['id']
    
    def __str__(self):
        if self.commenter == self.post.author:
            return self.commenter.username + " commented on his own post"
        else:
            return self.commenter.username + " commented on " + self.post.author.username + "'s post"