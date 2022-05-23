from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.models import *
from posts.models import *
from posts.forms import *
from notifications.models import *
from django.db.models import Q

from accounts.views import cheek_user_picture

# Create your views here.
def Reverse(lst):
    return [ele for ele in reversed(lst)]


@login_required(login_url='accounts:loginuser')
def Home_Page_views(request):
    
    cheek_user_picture(request)
    obj_user_posts = Post.objects.order_by('?')

    obj_user_posts = Reverse(obj_user_posts)


    comments_lenth = Post_Comments.objects.all()

    form = LikeForm_Profile()


    if request.method == "POST":
        form = LikeForm_Profile(request.POST)

        if request.POST.get('post_id') != None:
            cheek_user = Post_Like.objects.filter(liker_id=request.user.id, post_id=request.POST.get('post_id')) # Cheek If user has liked the post
            cheek_user = len(cheek_user)

            if cheek_user == 0:
                Post_Like.objects.create(liker_id=request.user.id, post_id=request.POST.get('post_id'))
                # Like
                if str(request.POST.get('post_author')) != str(request.user.id):
                        Notifications.objects.create(post_id=request.POST.get('post_id'), sender_id=request.user.id, user_id=request.POST.get('post_author'), notification_type=1, text_preview="Liked your post", date=request.POST.get("datenow"))
            else:
                Post_Like.objects.filter(liker_id=request.user.id, post_id=request.POST.get('post_id')).delete()
                if str(request.POST.get('post_author')) != str(request.user.id):
                        Notifications.objects.filter(post_id=request.POST.get('post_id'), sender_id=request.user.id, user_id=request.POST.get('post_author'), notification_type=1).delete()

                # Dislike

    cheek_like = Post_Like.objects.all()
    cheek_like_user = Post_Like.objects.filter(liker_id=request.user.id)

    max_likes =  Post_Like.objects.all()

    accounts_profile_image = Profile_picture.objects.all()


    get_posts_only_for_follower = list(Follow.objects.filter(follower=request.user.id))
    get_user_posts = list(Post.objects.filter(author_id=request.user.id))

    filter_all_posts = get_posts_only_for_follower + get_user_posts



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
        "accounts_profile_image":accounts_profile_image,
        "obj_user_posts":obj_user_posts,
        "profile_image": Profile_picture.objects.get(author_id=request.user.id).image.url,
        "form":form,
        "cheek_like":cheek_like,
        "cheek_like_user":cheek_like_user,
        "max_likes":max_likes,
        'comments_lenth':comments_lenth,
        'get_posts_only_for_follower':get_posts_only_for_follower,
        "filter_all_posts":filter_all_posts,
        "suggestions_id":suggestions_id,
        "suggestions_data":suggestions_data,
        "suggestions_image":suggestions_image,

        "notification_bar_len":notification_bar_len,
        "bell":bell,
        "theme":Profile_picture.objects.get(author_id=request.user.id).theme,

    }


    return render(request, 'home.html', context)


@login_required(login_url='accounts:loginuser')
def Search_Page_views(request):
    if request.method == "GET":
        # Search functionalty
        q = request.GET.get('q')
        if len(q) != 0:
            search_results = User.objects.filter(username__icontains=q)
        else:
            search_results = User.objects.all()

        accounts_profile_image = Profile_picture.objects.all()

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
        "profile_image": Profile_picture.objects.get(author_id=request.user.id).image.url,
        "search_results":search_results,
        "accounts_profile_image":accounts_profile_image,
        "suggestions_id":suggestions_id,
        "suggestions_data":suggestions_data,
        "suggestions_image":suggestions_image,
        "notification_bar_len":notification_bar_len,
        "bell":bell,
        "theme":Profile_picture.objects.get(author_id=request.user.id).theme,
        "search_query":q,

    }
    return render(request, 'search.html', context)

