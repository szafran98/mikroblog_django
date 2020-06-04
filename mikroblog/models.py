from django.db import models
from accounts.models import CustomUser


# Create your models here.


class Post(models.Model):
    content_post = models.TextField(default='', max_length=300)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    tags = models.CharField(max_length=50, default="")
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    liked = models.ManyToManyField('accounts.CustomUser', related_name='PostLikeToggle')

    class Meta:
        ordering = ['pub_date']

    @staticmethod
    def get_user_posts(username):
        return Post.objects.filter(author__username=username)

    @staticmethod
    def update_post_content(id, content):
        Post.objects.filter(id=id).update(content_post=content)

    @staticmethod
    def get_posts_on_specific_tag(tag, **kwargs):
        posts_except_blocked = Post.get_posts_except_blocked(kwargs.pop('user'))
        posts_on_tag = posts_except_blocked.filter(content_post__contains=tag)
        posts_on_tag = [specific_post for specific_post in posts_on_tag if tag in specific_post.content_post.split()]
        return posts_on_tag

    @staticmethod
    def get_posts_except_blocked(user):
        user = CustomUser.objects.get(username=user)
        blocked_users = user.blocked.all()
        return Post.objects.exclude(author__in=blocked_users).order_by('-pub_date')

    @staticmethod
    def get_specific_post(id):
        return Post.objects.get(id=id)

    @property
    def total_likes(self):
        return self.liked.count()

    def __str__(self):
        return f'{self.author}, {self.pub_date}'


class Comment(models.Model):
    content_comment = models.TextField(default='', max_length=100)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['pub_date']

    @staticmethod
    def get_user_comment_count(username):
        return Comment.objects.filter(author__username=username).count()

    @staticmethod
    def get_comments_to_post(to_post):
        return Comment.objects.filter(to_post=to_post)

    def __str__(self):
        return f'By: {self.author} To: {self.to_post.author} At date: {self.to_post.pub_date}'


class TalkAbout(models.Model):
    where = models.ForeignKey(Post, on_delete=models.CASCADE)
    _from = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='from_user')
    to = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='to_user')
