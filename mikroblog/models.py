from django.db import models


# Create your models here.


class Post(models.Model):
    content_post = models.TextField(default='', max_length=300)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    tags = models.CharField(max_length=50, default="")
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    liked = models.ManyToManyField('accounts.CustomUser', related_name='PostLikeToggle')

    class Meta:
        ordering = ['pub_date']

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

    def __str__(self):
        return f'By: {self.author} To: {self.to_post.author} At date: {self.to_post.pub_date}'


class TalkAbout(models.Model):
    where = models.ForeignKey(Post, on_delete=models.CASCADE)
    _from = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='from_user')
    to = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='to_user')
