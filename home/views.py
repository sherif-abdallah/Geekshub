from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from accounts.models import *
from posts.models import *
from posts.forms import *
from notifications.models import *
from social.defMain import *

# Create your views here.
@login_required(login_url='accounts:loginuser')
def Home_Page_views(request):
    
    cheek_user_picture(request)
    check_if_company_account_didnt_send_to_user(request)

    # get all posts from following users
    news_feed = Follow.objects.filter(follower=request.user.id)
    news_feed = list(news_feed.values_list('following', flat=True))
    news_feed.append(int(request.user.id))
    news_feed = listToStringWithoutBrackets(news_feed)
    news_feed_sql = Post.objects.raw("SELECT * FROM posts_post WHERE author_id IN (" + news_feed +")")
    news_feed = Reverse(news_feed_sql)
    news_feed = paginate(request, posts=news_feed, num_posts=5)


    
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


    # Get Likes length per post
    max_likes =  Post_Like.objects.values("post_id").annotate(the_count=Count("post_id"))
    # Get Comments length per post
    comments_lenth = Post_Comments.objects.values("post_id").annotate(the_count=Count("post_id"))
    

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
        "accounts_profile_image":accounts_profile_image,
        "news_feed":news_feed,
        "profile_image": Profile_picture.objects.get(author_id=request.user.id).image.url,
        "form":form,
        "cheek_like":cheek_like,
        "cheek_like_user":cheek_like_user,
        "max_likes":max_likes,
        'comments_lenth':comments_lenth,
        "suggestions_id":suggestions_id,
        "suggestions_data":suggestions_data,
        "suggestions_image":suggestions_image,
        "notification_bar_len":notification_bar_len,
        "bell":bell,
        "theme":Profile_picture.objects.get(author_id=request.user.id).theme,
        "last_msg_friend_id":Last_Messages_Friend_id(request),
        "message_notification_len": Message_Notification_views(request),

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


    search_results = paginate(request, search_results, 10)

    if len(search_results) == 0:
        noResults = True
    else:
        noResults = False


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
        "last_msg_friend_id":Last_Messages_Friend_id(request),
        "message_notification_len": Message_Notification_views(request),
        "noResults":noResults,

    }
    return render(request, 'search.html', context)


def Redirect_favicon_View(request):
    return redirect('/static/logo/favicon.ico')