from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .models import Post, Comment, TalkAbout
from accounts.models import CustomUser
from .forms import AddPostForm, AddCommentForm


# Create your views here.

def view_common(url, request, tag=None, username=None, id=None):
    post_form = AddPostForm(request.POST or None, instance=request.user)
    comment_form = AddCommentForm(request.POST or None, instance=request.user)

    if request.method == 'POST':
        # FORMULARZ DODAWANIA POSTU
        if post_form.is_valid():
            post_form.save()
            # create_notifications(post_form.instance)

        # FORMULARZ DODAWANIA KOMENTARZA
        if comment_form.is_valid():
            comment_form.save()

    if request.user.is_authenticated:
        posts = Post.get_posts_except_blocked(request.user)
        comments = Comment.objects.all().order_by('-pub_date')
    else:
        posts = Post.objects.all().order_by('-pub_date')
        comments = Comment.objects.all().order_by('-pub_date')

    parameters = {'posts': posts, 'comments': comments, 'post_form': post_form, 'comment_form': comment_form}

    if tag:
        posts_on_tag = Post.get_posts_on_specific_tag(tag, user=request.user)
        parameters.update({'actual_tag': tag, 'posts': posts_on_tag})

    if username:
        try:
            filtered_posts = Post.get_user_posts(username)
            user_data = CustomUser.objects.get(username=username)
            user_comments_count = Comment.get_user_comment_count(username)
            values_to_update = {'user_data': user_data, 'user_comments_count': user_comments_count,
                                'posts': filtered_posts}
            parameters.update(values_to_update)
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'User does not exist!')
            return HttpResponseRedirect(reverse('index'))

    if id:
        try:
            specific_post = Post.get_specific_post(id)
            comments_to_post = Comment.get_comments_to_post(specific_post)
            parameters['post'] = specific_post
            parameters['comments'] = comments_to_post
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Post does not exist!')
            return HttpResponseRedirect(reverse('index'))

    return render(request, url, parameters)


def index(request):
    return view_common('mikroblog/index.html', request)


def tag_view(request, tag):
    return view_common('mikroblog/tag.html', request, tag=tag)


def profile_view(request, username):
    return view_common('mikroblog/profile.html', request, username=username)


def post_view(request, id):
    return view_common('mikroblog/post_details.html', request, id=id)


@login_required
def delete_post(request, id):
    post_to_delete = Post.objects.get(id=id)
    if request.method == 'DELETE':
        post_to_delete.delete()

        return redirect('index')


@login_required
def edit_post(request, id):
    edited_post = Post.objects.get(id=id)
    post_form = AddPostForm(request.POST or None, instance=request.user)
    if request.POST:
        if post_form.is_valid():
            new_content_post = post_form.cleaned_data.get('content_post')
            Post.update_post_content(id, new_content_post)
            # create_notifications(edited_post)
            return HttpResponseRedirect(reverse('post', kwargs={'id': id}))

    return render(request, 'mikroblog/edit.html', {'post': edited_post, 'post_form': post_form})


@login_required
def post_like_toggle(request):
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

    if request.method == 'GET':
        notifications = TalkAbout.objects.all().filter(to=user)
        json_to_send = []

        for notification in notifications:
            json = {'id': notification.id, 'from': notification._from.username, 'to': notification.to.username,
                    'where': notification.where.id}
            json_to_send.append(json)

        return JsonResponse({'notifications': json_to_send})


@login_required
def delete_notification(request, id):
    notification_to_delete = TalkAbout.objects.get(id=id)
    if request.method == 'DELETE':
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

    if request.method == 'GET':
        user_blacklist = user.blocked.all()

        json_to_send = []

        for blacklist_entry in user_blacklist:
            json = {'id': blacklist_entry.id, 'blocked': blacklist_entry.username}
            json_to_send.append(json)

        return JsonResponse({'blackList': json_to_send})


@login_required
def remove_from_blacklist(request, id):
    user = CustomUser.objects.get(id=request.user.id)

    if request.method == 'DELETE':
        blacklist_entry_to_delete = user.blocked.get(id=id)
        user.blocked.remove(blacklist_entry_to_delete)

        return HttpResponseRedirect(reverse('index'))


@receiver(post_save, sender=Post)
def create_notifications(instance, **kwargs):
    for word in instance.content_post.split():
        if '@' in word:
            try:
                user_to_notificate = CustomUser.objects.get(username=word[1:])
                TalkAbout(where=instance, _from=instance.author, to=user_to_notificate).save()
            except ObjectDoesNotExist:
                return HttpResponseRedirect(reverse('index'))
