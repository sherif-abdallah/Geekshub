from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from accounts.models import *
from posts.models import *
from posts.forms import *
from notifications.models import *
from social.defMain import cheek_user_picture, paginate, Reverse, listToStringWithoutBrackets

# Create your views here.
@login_required(login_url='accounts:loginuser')
def Home_Page_views(request):
    
    cheek_user_picture(request)


    # get all posts from following users
    news_feed = Follow.objects.filter(follower=request.user.id)
    news_feed = list(news_feed.values_list('following', flat=True))
    news_feed.append(int(request.user.id))
    news_feed = listToStringWithoutBrackets(news_feed)
    news_feed_sql = Post.objects.raw("SELECT * FROM posts_post WHERE author_id IN (" + news_feed +")")
    news_feed = Reverse(news_feed_sql)
    news_feed = paginate(request, posts=news_feed, num_posts=15)


    # the posts well be randomed in the template

    
    form = LikeForm_Profile()

    if request.method == "POST":
        form = LikeForm_Profile(request.POST)


        # If user Press Like button
        if request.POST.get('post_like_id') != None:
            cheek_user_like = Post_Like.objects.filter(liker_id=request.user.id, post_id=request.POST.get('post_like_id')) # Cheek If user has liked the post
            cheek_user_like = len(cheek_user_like)

            if cheek_user_like == 0:
                # Like
                Post_Like.objects.create(liker_id=request.user.id, post_id=request.POST.get('post_like_id'))
                if str(request.POST.get('post_author')) != str(request.user.id):
                        Notifications.objects.create(post_id=request.POST.get('post_like_id'), sender_id=request.user.id, user_id=request.POST.get('post_author'), notification_type=1, text_preview="Liked your post", date=request.POST.get("datenow"))
            else:
                # Dislike
                Post_Like.objects.filter(liker_id=request.user.id, post_id=request.POST.get('post_like_id')).delete()
                if str(request.POST.get('post_author')) != str(request.user.id):
                        Notifications.objects.filter(post_id=request.POST.get('post_like_id'), sender_id=request.user.id, user_id=request.POST.get('post_author'), notification_type=1).delete()
        
        
        # If user Press Add Fav Button
        if request.POST.get('post_fav_id') != None:
            cheek_user_fav = Post_Favorite.objects.filter(user_id=request.user.id, post_id=request.POST.get('post_fav_id')) # Cheek If user has liked the post
            cheek_user_fav = len(cheek_user_fav)

            if cheek_user_fav == 0:
                # Like
                Post_Favorite.objects.create(user_id=request.user.id, post_id=request.POST.get('post_fav_id'))
            else:
                # Dislike
                Post_Favorite.objects.filter(user_id=request.user.id, post_id=request.POST.get('post_fav_id')).delete()


    cheek_like_user = Post_Like.objects.filter(liker_id=request.user.id)
    cheek_fav_user = Post_Favorite.objects.filter(user_id=request.user.id)


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
        "cheek_like_user":cheek_like_user,
        "cheek_fav_user":cheek_fav_user,
        "max_likes":max_likes,
        'comments_lenth':comments_lenth,
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

        search_results_length = len(search_results)
        accounts_profile_image = Profile_picture.objects.all()




    search_results = paginate(request, search_results, 10)
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
        "search_results_length":search_results_length,
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

