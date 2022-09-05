from unicodedata import name
from django.db import models
# comment this line for now from django.contrib.auth.models import User, AbstractUser

# Create your models here.
THEME_CHOICE = (
    ('Light Mode', 'Light Mode'),
    ('Dark Mode', 'Dark Mode'),
)

#model for profile setting
class Setting(models.Model):
    theme = models.CharField(max_length=1000, choices=THEME_CHOICE, default='Light Mode')
    profile=models.OneToOneField()


#models for groups
class Group(models.Model):
    name=models.CharField(max_length=100)
    bio=models.TextField(null=True,blank=True)
    created_on=models.DateField(auto_now_add=True)
    website=models.URLField(null=True,blank=True)
    members=models.ManyToManyField("profile", related_name = 'member',symmetrical=False)
    def __str__(self) -> str:
        return  self.name

#models for user profile
class  Profile(models.Model):
    user=models.OneToOneField('auth.User',on_delete=models.CASCADE)
    pseudo=models.CharField(max_length=100)
    bio=models.TextField(null=True,blank=True)
    website=models.URLField(blank=True,null=True)
    inscription_date=models.DateField(auto_now_add=True)
    Profile_picture=models.ImageField(upload_to="profile",default="posts/default.jpg")
    follows = models.ManyToManyField("self", related_name = 'follows',symmetrical=False)
    

    setting=models.OneToOneField(Setting,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.pseudo
