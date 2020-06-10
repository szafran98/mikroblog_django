from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse

from accounts.models import CustomUser


# Create your models here.


class Post(models.Model):
    content_post = models.TextField(default='', max_length=300)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    liked = models.ManyToManyField('accounts.CustomUser', related_name='PostLikeToggle')

    class Meta:
        ordering = ['pub_date']

    @staticmethod
    def get_user_posts(user):
        return Post.objects.filter(author=user)

    def update_post_content(self, content):
        if len(content) <= self.__len__():
            self.content_post = content
            self.save()
        else:
            return Exception

    def __len__(self):
        return self._meta.get_field('content_post').max_length

    @staticmethod
    def get_posts_except_blocked(user):
        blocked_users = user.blocked.all()
        return Post.objects.exclude(author__in=blocked_users)

    @classmethod
    def get_specific_post(cls, id):
        return cls.objects.get(id=id)

    @property
    def total_likes(self):
        return self.liked.count()

    def __str__(self):
        return f'{self.author}, {self.pub_date}'


def get_posts_on_specific_tag(tag, posts):
    posts_on_tag = posts.filter(content_post__contains=tag)
    posts_on_tag = [specific_post for specific_post in posts_on_tag if tag in specific_post.content_post.split()]
    return posts_on_tag


class Comment(models.Model):
    content_comment = models.TextField(default='', max_length=100)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['pub_date']

    @staticmethod
    def get_user_comment_count(user):
        return Comment.objects.filter(author=user).count()

    @staticmethod
    def get_comments_to_post(to_post):
        return Comment.objects.filter(to_post=to_post)

    def __str__(self):
        return f'By: {self.author} To: {self.to_post.author} At date: {self.to_post.pub_date}'


class TalkAbout(models.Model):
    where = models.ForeignKey(Post, on_delete=models.CASCADE)
    _from = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='from_user')
    to = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='to_user')

