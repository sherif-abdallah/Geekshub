from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from posts.models import Post
from django.contrib.auth.models import User
from .models import Follow, Profile_picture
from django.db.models import Count
from posts.forms import *
from .forms import *
from posts.models import *
from notifications.models import *
from social.defMain import paginate, cheek_user_picture, check_email_is_valid, Reverse



# Create your views here.
def register(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        username_error = "" if request.POST.get('username') == None else request.POST.get('username')
        email_error = "" if request.POST.get('email') == None else request.POST.get('email')


        if form.is_valid():
            email = request.POST.get('email')
            if check_email_is_valid(email) == True:
                if User.objects.filter(email=email).exists() == False:
                    form.save()
                    userid = form.save().id
                    User.objects.filter(id=userid).update(email=email)
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password1']

                    user = authenticate(username=username, password=password)
                    login(request, user)
                    Profile_picture.objects.create(author_id=request.user.id)

                    return redirect('home:homepage')
                else:
                    form = UserCreationForm()
                    message = "The email is already taken"
            else:
                form = UserCreationForm()
                message = "Please write a valid email"
        else:
            message = ""

    else:
        form = UserCreationForm()
        message = ""
        username_error = ""
        email_error = ""




    context = {
        'form':form,
        'message':message,
        "username_error":username_error,
        "email_error":email_error,
    }
    
    
    return render(request, 'signup.html', context)



@login_required(login_url='accounts:loginuser')
def Profile_views(request, userid):

    cheek_user_picture(request)

    obj_user_posts = Post.objects.filter(author_id=userid)
    obj_user_posts = Reverse(obj_user_posts)
    obj_user_posts = paginate(request, posts=obj_user_posts, num_posts=15)
    
    account_username =  User.objects.get(id=userid).username
    accounts_profile_image = Profile_picture.objects.get(author_id=userid).image.url
    cheek_if_no_post = Post.objects.filter(author_id=userid)



    if len(cheek_if_no_post) == 0:
        cheek_if_no_post = 'The User dosent have any post yet'
    else:
        cheek_if_no_post = ''



    form = LikeForm_Profile()

    cheek_if_follow = Follow.objects.filter(follower_id=request.user.id, following_id=userid)
    if len(cheek_if_follow) == 0:
        follow_message = 'Follow'
    elif len(cheek_if_follow) != 0:
        follow_message = 'Unfollow'

    # Cheek Followers
    cheek_followers = Follow.objects.filter(following_id=userid)
    max_cheek_followers = len(cheek_followers)
    cheek_following = Follow.objects.filter(follower_id=userid)
    max_cheek_following = len(cheek_following)


    if request.method == "POST":

        form = LikeForm_Profile(request.POST)
        if request.POST.get('follow_valid') == "True":
            cheek_if_follow = Follow.objects.filter(follower_id=request.user.id, following_id=userid)

            if len(cheek_if_follow) == 0:
                Follow.objects.create(follower_id=request.user.id, following_id=userid)
                follow_message = 'Unfollow'
                Notifications.objects.create(sender_id=request.user.id, user_id=userid, notification_type=3, text_preview="Started Following you", date=request.POST.get("datenow"))

            elif len(cheek_if_follow) != 0:
                Follow.objects.filter(follower_id=request.user.id, following_id=userid).delete()
                follow_message = 'Follow'
                Notifications.objects.filter(sender_id=request.user.id, user_id=userid, notification_type=3).delete()
    
        if request.POST.get('post_id') != None:
            cheek_user = Post_Like.objects.filter(liker_id=request.user.id, post_id=request.POST.get('post_id')) # Cheek If user has liked the post
            cheek_user = len(cheek_user)

            if cheek_user == 0:
                Post_Like.objects.create(liker_id=request.user.id, post_id=request.POST.get('post_id'))
                if str(request.POST.get('post_author')) != str(request.user.id):
                    Notifications.objects.create(post_id=request.POST.get('post_id'), sender_id=request.user.id, user_id=request.POST.get('post_author'), notification_type=1, text_preview="Liked your post", date=request.POST.get("datenow"))

                # Like
            else:
                Post_Like.objects.filter(liker_id=request.user.id, post_id=request.POST.get('post_id')).delete()

                if str(request.POST.get('post_author')) != str(request.user.id):
                    Notifications.objects.filter(post_id=request.POST.get('post_id'), sender_id=request.user.id, user_id=request.POST.get('post_author'), notification_type=1).delete()

                # Dislike

    cheek_like = Post_Like.objects.all()
    cheek_like_user = Post_Like.objects.filter(liker_id=request.user.id)

    # Get Likes length per post
    max_likes =  Post_Like.objects.values("post_id").annotate(the_count=Count("post_id"))
    # Get Comments length per post
    comments_lenth = Post_Comments.objects.values("post_id").annotate(the_count=Count("post_id"))
    



    # Suggestions For You
    suggestions = Follow.objects.values_list('following').annotate(most=Count('following')).order_by('-most')[:3]
    suggestions_id = [a_tuple[0] for a_tuple in suggestions]
    suggestions_data = User.objects.all()
    suggestions_image = Profile_picture.objects.all()

    #notification_bar
    notification_bar = Notifications.objects.filter(user=request.user.id, is_seen=False)
    notification_bar_len = len(notification_bar)
    if notification_bar_len == 0:
        bell = False
    else:
        bell = True

    context = {
        "obj_user_posts":obj_user_posts,
        "accounts_profile_image":accounts_profile_image,
        "profile_image": Profile_picture.objects.get(author_id=request.user.id).image.url,  
        "cheek_if_no_post":cheek_if_no_post,
        "account_username":account_username,

        "form":form,
        "cheek_like":cheek_like,
        "cheek_like_user":cheek_like_user,
        "max_likes":max_likes,
        "userid":userid,
        'comments_lenth':comments_lenth,
        'follow_message':follow_message,
        'max_cheek_followers':max_cheek_followers,
        'max_cheek_following':max_cheek_following,
        "suggestions_id":suggestions_id,
        "suggestions_data":suggestions_data,
        "suggestions_image":suggestions_image,
        "notification_bar_len":notification_bar_len,
        "bell":bell,
        "theme":Profile_picture.objects.get(author_id=request.user.id).theme

    }


    return render(request, 'profile.html', context)

@login_required(login_url='accounts:loginuser')
def Edit_Profile_views(request):

    cheek_user_picture(request)

    form = Edit_Profile_Form()
    if request.method == "POST":
        form = Edit_Profile_Form(request.POST, request.FILES)

        username = request.user
        email = request.user.email
        
        if form.is_valid():
            image = form.cleaned_data['image']

            if len(form.cleaned_data['username']) != 0:         
                obj = User.objects.get(id=request.user.id)
                obj.username = form.cleaned_data['username']
                obj.save()
                username = form.cleaned_data['username']

            email = request.POST.get('email')

            if len(request.POST.get('email')) != 0:   
                if check_email_is_valid(email) == True:
                    if User.objects.filter(email=email).exists() == False:
                        email = User.objects.get(id=request.user.id)
                        email.email = request.POST.get('email')
                        email.save()
                        email = request.POST.get('email')
                        message = "Done"
                    else:
                        message = "The email is already taken"
                else:
                    message = "Please write a valid email"
            else:
                message = ""


            if image != None:

                Profile_picture.objects.filter(author_id=request.user.id).delete()
                Profile_picture.objects.create(author_id=request.user.id, image=image)
            Profile_picture.objects.filter(author_id=request.user.id).update(theme=request.POST.get('theme'))
            cheek_theme = request.POST.get('theme')                
    else:
        username = request.user
        
        email = request.user.email
        cheek_theme = Profile_picture.objects.get(author_id=request.user.id).theme
        message = ""


    image = Profile_picture.objects.get(author_id=request.user.id)

    #notification_bar
    notification_bar = Notifications.objects.filter(user=request.user.id, is_seen=False)
    notification_bar_len = len(notification_bar)
    if notification_bar_len == 0:
        bell = False
    else:
        bell = True



    context = {
        "form":form,
        "username":username,
        "image":image,
        "profile_image": Profile_picture.objects.get(author_id=request.user.id).image.url,
        "notification_bar_len":notification_bar_len,
        "bell":bell,
        "cheek_theme":cheek_theme,
        "theme":Profile_picture.objects.get(author_id=request.user.id).theme,
        "email":email,
        "message":message,
        
    }

    return render(request, 'edit_profile.html', context)

