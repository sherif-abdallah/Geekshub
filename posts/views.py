from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accounts.models import Profile_picture
from django.contrib.auth.models import User
from .forms import *
from .models import *
from notifications.models import *
from accounts.models import *
from social.defMain import *



# Create your views here.
@login_required(login_url='accounts:loginuser')
def Post_create_views(request):
    cheek_user_picture(request)
    check_if_company_account_didnt_send_to_user(request)


    post_form = PostForm()
    if request.method == 'POST':

        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            Post.objects.create(author_id=request.user.id, body=post_form.cleaned_data["body"], image=post_form.cleaned_data['image'], created_on=request.POST.get('created_on'))
            
            return redirect('home:homepage')
        

    #notification_bar
    notification_bar = Notifications.objects.filter(user=request.user.id, is_seen=False)
    notification_bar_len = len(notification_bar)
    if notification_bar_len == 0:
        bell = False
    else:
        bell = True

    context = {
        "post_form":post_form,
        "profile_image": Profile_picture.objects.get(author_id=request.user.id).image.url,
        "notification_bar_len":notification_bar_len,
        "bell":bell,
        "theme":Profile_picture.objects.get(author_id=request.user.id).theme,
        "last_msg_friend_id":Last_Messages_Friend_id(request),
        "message_notification_len": Message_Notification_views(request),
    }


    return render(request, "create_post.html", context)

@login_required(login_url='accounts:loginuser')
def Post_views(request, id):
    cheek_user_picture(request)
    check_if_company_account_didnt_send_to_user(request)

    post = Post.objects.get(id=id)
    username_id = Post.objects.get(id=id).author.id
    image_user_profile_picture = Profile_picture.objects.get(author_id=username_id).image.url

    # Like Object
    cheek_user = Post_Like.objects.filter(liker_id=request.user.id, post_id=post.id) # Cheek If user has liked the post
    cheek_user = len(cheek_user)
    

    # Comment Object
    all_post_comments = Post_Comments.objects.filter(post_id=id)
    all_post_comments = paginate(request, all_post_comments, 10)

    commenter_profile_picture = Profile_picture.objects.all()

    if request.method == "POST":
        # If Like Form Is Submited

        if request.POST.get('post_valid') == "True":
            cheek_user = Post_Like.objects.filter(liker_id=request.user.id, post_id=post.id) # Cheek If user has liked the post
            cheek_user = len(cheek_user)

            if cheek_user == 0:
                Post_Like.objects.create(liker_id=request.user.id, post_id=post.id)
                if post.author.id != request.user.id:
                    Notifications.objects.create(post_id=post.id, sender_id=request.user.id, user_id=post.author.id, notification_type=1, text_preview="Liked your post", date=request.POST.get("datenow"))
                # Like
            else:
                Post_Like.objects.filter(liker_id=request.user.id, post_id=post.id).delete()
                if post.author.id != request.user.id:
                    Notifications.objects.filter(post_id=post.id, sender_id=request.user.id, user_id=post.author.id, notification_type=1).delete()
                # Dislike
        # If Comment for is Submited
        if request.POST.get('comment_valid') == "True":
            create_comment = Post_Comments.objects.create(commenter=request.user, comment_body=request.POST.get('commentvalue'), post_id=id, creared_on=request.POST.get('created_on_comment'))
            if post.author.id != request.user.id:
                    Notifications.objects.create(post_id=id, sender_id=request.user.id, comment_id=create_comment.id , user_id=post.author.id, notification_type=2, text_preview="Commented on your post", date=request.POST.get("datenow"))

        if request.POST.get('comment_delete_valid') == "True":
            comment_delete_id = request.POST.get('comment_delete_id')
            Post_Comments.objects.filter(id=comment_delete_id).delete()
            if post.author.id != request.user.id:
                    Notifications.objects.filter(post_id=id, sender_id=request.user.id, comment_id=comment_delete_id , user_id=post.author.id, notification_type=2).delete()


    max_likes = len(Post_Like.objects.filter(post_id=post.id))
    
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
        "post":post,
        "profile_image": Profile_picture.objects.get(author_id=request.user.id).image.url,
        "image_user_profile_picture":image_user_profile_picture,
        "cheek_user":cheek_user,
        "max_likes":max_likes,
        'all_post_comments':all_post_comments,
        'commenter_profile_picture':commenter_profile_picture,
        "suggestions_id":suggestions_id,
        "suggestions_data":suggestions_data,
        "suggestions_image":suggestions_image,
        "notification_bar_len":notification_bar_len,
        "bell":bell,
        "theme":Profile_picture.objects.get(author_id=request.user.id).theme,
        "last_msg_friend_id":Last_Messages_Friend_id(request),
        "message_notification_len": Message_Notification_views(request),

    }
    return render(request, "post.html", context)

@login_required(login_url='accounts:loginuser')
def Delete_Post_views(request, id):
    cheek_user_picture(request)
    check_if_company_account_didnt_send_to_user(request)

    obj = Post.objects.get(id=id)
    if request.user.id == obj.author_id:
        obj.delete()
        
        message = "Your Post was deleted"
        return redirect('/')
    else:
        message = "Erorr 404"

    return render(request, 'delete_post.html', {"message":message})

@login_required(login_url='accounts:loginuser')
def Edit_Post_views(request, id):
    
    cheek_user_picture(request)

    post_detaild_before = Post.objects.get(id=id) # Post Body Before Edit

    if request.user.id == post_detaild_before.author_id:
        post_form = EditPost()
        if request.method == "POST":
            post_form = EditPost(request.POST, request.FILES)
            if post_form.is_valid():
                if post_form.cleaned_data['image'] != None:
                    # Edit The All Of the Post if All input is Good
                    edit_full_post = Post.objects.get(id=id)
                    edit_full_post.image = post_form.cleaned_data['image']
                    edit_full_post.body = post_form.cleaned_data['body']
                    edit_full_post.save()
                elif post_form.cleaned_data['image'] == None:
                    edit_post_body = Post.objects.get(id=id)
                    edit_post_body.body = post_form.cleaned_data['body']
                    edit_post_body.save()
                return redirect(reverse("posts:post", args=[id]))
        # redirect(reverse('test:output_page', args=instance))

    #notification_bar
    notification_bar = Notifications.objects.filter(user=request.user.id, is_seen=False)
    notification_bar_len = len(notification_bar)
    if notification_bar_len == 0:
        bell = False
    else:
        bell = True

    context = {
        "post_form":post_form,
        "post_detaild_before":post_detaild_before,  
        "profile_image": Profile_picture.objects.get(author_id=request.user.id).image.url, "post_id":id,
        "notification_bar_len":notification_bar_len,
        "bell":bell,
        "theme":Profile_picture.objects.get(author_id=request.user.id).theme,
        "last_msg_friend_id":Last_Messages_Friend_id(request),
        "message_notification_len": Message_Notification_views(request),


        }

    return render(request, 'edit_post.html', context)

def Main_Post_URL(request):
    return render(request, 'ondateup.html')