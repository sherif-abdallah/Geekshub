from accounts.models import Profile_picture
from django.core.paginator import Paginator
import re


# Create your Packages here.
def check_email_is_valid(email):  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex, email)):   
        return True
    else:
        return False


# Cheek if user dosent have profile picture
def cheek_user_picture(request):
    profile_picture = Profile_picture.objects.filter(author_id=request.user)
    if len(profile_picture) == 0:
        Profile_picture.objects.create(author_id=request.user.id)

# Paginate the posts
def paginate(request, posts, num_posts):
    paginator = Paginator(posts, num_posts)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return posts

def Reverse(lst):
    return [ele for ele in reversed(lst)]

def listToStringWithoutBrackets(lst):
    return str(lst).replace('[','').replace(']','')

