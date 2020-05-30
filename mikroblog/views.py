from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse
from .models import Post, Comment, TalkAbout
from accounts.models import CustomUser
from .forms import AddPostForm, AddCommentForm


# Create your views here.

def index(request):
    new_post = None
    new_comment = None
    if request.method == 'POST':
        post_form = AddPostForm(request.POST)
        comment_form = AddCommentForm(request.POST)
        # FORMULARZ DODAWANIA POSTU
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.tags = ''
            # content = new_post.content_post
            content = ''
            # CHECK TAGS
            for word in new_post.content_post.split():
                if '#' in word:
                    # tag_length = len(word) + 1
                    new_post.tags += f"{word} "
                    content += f"{word} "
                    # new_post.content_post = new_post.content_post[:-tag_length]
                else:
                    content += f"{word} "
            # CHECK ADDED NOTIFICATION

            new_post.content_post = content
            new_post.save()

            for word in content.split():
                if '@' in word:
                    print(word)
                    user_to_notificate = CustomUser.objects.get(username=word[1:])

                    new_notification = TalkAbout()
                    new_notification.where = new_post
                    new_notification._from = new_post.author
                    new_notification.to = user_to_notificate
                    new_notification.sended = False
                    print(new_notification)
                    new_notification.save()

            post_form = AddPostForm()

        # FORMULARZ DODAWANIA KOMENTARZA
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            # new_comment.to_post = Post.objects.get()
            new_comment.save()
            comment_form = AddCommentForm()
    else:
        post_form = AddPostForm()
        comment_form = AddCommentForm()

    if request.user.is_authenticated:
        logged_user = CustomUser.objects.get(id=request.user.id)
        blocked_users = logged_user.blocked.all()
        posts = Post.objects.exclude(author__in=blocked_users)
        print(blocked_users)
        posts = posts.order_by('-pub_date')
    else:
        posts = Post.objects.all()
        posts = posts.order_by('-pub_date')

    comments = Comment.objects.all()
    comments = comments.order_by("-pub_date")

    # post_likes = post.liked.count()

    return render(request, 'mikroblog/index.html', {'posts': posts, 'comments': comments,
                                                    'post_form': post_form, 'comment_form': comment_form})


def tag_view(request, tag):
    # tag = request.get_full_path()
    new_post = None
    new_comment = None
    if request.method == 'POST':
        post_form = AddPostForm(request.POST)
        comment_form = AddCommentForm(request.POST)
        # FORMULARZ DODAWANIA POSTU
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.tags = ''
            # content = new_post.content_post
            content = ''
            for word in new_post.content_post.split():
                if '#' in word:
                    # tag_length = len(word) + 1
                    new_post.tags += f"{word} "
                    # new_post.content_post = new_post.content_post[:-tag_length]
                else:
                    content += f"{word} "
            new_post.content_post = content
            new_post.save()
            post_form = AddPostForm()

        # FORMULARZ DODAWANIA KOMENTARZA
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            # new_comment.to_post = Post.objects.get()
            new_comment.save()
            comment_form = AddCommentForm()
    else:
        post_form = AddPostForm()
        comment_form = AddCommentForm()

    posts = Post.objects.all().filter(tags__contains=tag)
    posts = posts.order_by('-pub_date')
    actual_tag = tag
    comments = Comment.objects.all()
    comments = comments.order_by("-pub_date")

    return render(request, 'mikroblog/tag.html', {'posts': posts, 'actual_tag': actual_tag, 'comments': comments,
                                                  'post_form': post_form, 'comment_form': comment_form})


def profile_view(request, username):
    new_post = None
    new_comment = None
    if request.method == 'POST':
        post_form = AddPostForm(request.POST)
        comment_form = AddCommentForm(request.POST)
        # FORMULARZ DODAWANIA POSTU
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.tags = ''
            # content = new_post.content_post
            content = ''
            for word in new_post.content_post.split():
                if '#' in word:
                    # tag_length = len(word) + 1
                    new_post.tags += f"{word} "
                    # new_post.content_post = new_post.content_post[:-tag_length]
                else:
                    content += f"{word} "
            new_post.content_post = content
            new_post.save()
            post_form = AddPostForm()

        # FORMULARZ DODAWANIA KOMENTARZA
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            # new_comment.to_post = Post.objects.get()
            new_comment.save()
            comment_form = AddCommentForm()
    else:
        post_form = AddPostForm()
        comment_form = AddCommentForm()

    posts = Post.objects.all().filter(author__username=username)
    posts = posts.order_by('-pub_date')
    user_profile_data = CustomUser.objects.get(username=username)
    comments = Comment.objects.all()
    comments = comments.order_by("-pub_date")
    user_comments_count = comments.filter(author__username=username).count()

    return render(request, 'mikroblog/profile.html',
                  {'posts': posts, 'user_profile_data': user_profile_data, 'comments': comments,
                   'post_form': post_form, 'comment_form': comment_form,
                   'user_comments_count': user_comments_count})


def post_view(request, id):
    new_comment = None
    if request.method == 'POST':
        comment_form = AddCommentForm(request.POST)

        # FORMULARZ DODAWANIA KOMENTARZA
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            # new_comment.to_post = Post.objects.get()
            new_comment.save()
            comment_form = AddCommentForm()
    else:
        comment_form = AddCommentForm()

    post = Post.objects.get(id=id)
    # post = post.order_by('-pub_date')

    comments = Comment.objects.all().filter(to_post=post)
    comments = comments.order_by("-pub_date")

    return render(request, 'mikroblog/post_details.html',
                  {'post': post, 'comments': comments, 'comment_form': comment_form})


@login_required
def delete_post(request, id):
    post_to_delete = Post.objects.get(id=id)
    if post_to_delete.author.username == request.user.username:
        post_to_delete.delete()
    return HttpResponseRedirect(reverse('index'))


@login_required
def edit_post(request, id):
    post_to_edit = Post.objects.get(id=id)
    post_comments = Comment.objects.all().filter(to_post=post_to_edit)
    if request.POST:
        post_form = AddPostForm(request.POST)

        if post_form.is_valid():
            form_data = post_form.save(commit=False)
            post_to_edit.author = request.user
            post_to_edit.tags = ''
            # content = new_post.content_post
            content = ''
            for word in form_data.content_post.split():
                if '#' in word:
                    # tag_length = len(word) + 1
                    post_to_edit.tags += f"{word} "
                    # new_post.content_post = new_post.content_post[:-tag_length]
                else:
                    content += f"{word} "
            post_to_edit.content_post = content
            post_to_edit.save()
            post_form = AddPostForm()
            return HttpResponseRedirect(reverse('post', kwargs={'id': id}))
    else:
        post_form = AddPostForm()

    return render(request, 'mikroblog/edit.html',
                  {'post': post_to_edit, 'comments': post_comments, 'post_form': post_form})


@login_required
def PostLikeToggle(request):
    user = request.user

    if request.method == 'POST':
        post_id = request.POST['post_id']

        post = Post.objects.get(id=post_id)

        _liked = user in post.liked.all()

        if _liked:
            post.liked.remove(user)

        else:
            post.liked.add(user)

        post_likes = post.liked.count()

        return JsonResponse({'liked': _liked, 'numOfLikes': post_likes})


@login_required
def check_notifications(request):
    user = request.user

    if request.method == 'POST':
        notifications = TalkAbout.objects.all().filter(to=user)
        json_to_send = []

        for notification in notifications:
            tmp = {'id': notification.id, 'from': notification._from.username, 'to': notification.to.username,
                   'where': notification.where.id}
            json_to_send.append(tmp)

        print(json_to_send)
        return JsonResponse({'notifications': json_to_send})


@login_required
def delete_notification(request, id):
    notification_to_delete = TalkAbout.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        notification_to_delete.delete()

    return HttpResponseRedirect(reverse('index'))


@login_required
def block_user(request, id):
    user = CustomUser.objects.get(id=request.user.id)
    user_to_be_blocked = CustomUser.objects.get(id=id)

    user.blocked.add(user_to_be_blocked)

    return HttpResponseRedirect(reverse('index'))


@login_required
def check_blacklist(request):
    user = CustomUser.objects.get(id=request.user.id)

    if request.method == 'POST':
        user_blacklist = user.blocked.all()

        json_to_send = []

        for blacklist_entry in user_blacklist:
            tmp = {'id': blacklist_entry.id, 'blocked': blacklist_entry.username}
            json_to_send.append(tmp)

        print(json_to_send)
        return JsonResponse({'blackList': json_to_send})


@login_required
def remove_from_blacklist(request, id):
    user = CustomUser.objects.get(id=request.user.id)

    if request.method == 'POST':
        blacklist_entry_to_delete = user.blocked.get(id=id)
        user.blocked.remove(blacklist_entry_to_delete)

        return HttpResponseRedirect(reverse('index'))
