from django import forms
from django.template.context_processors import request
from accounts.models import CustomUser

from .models import Post, Comment


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ['content_post', ]

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('instance')
        super(AddPostForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.author = self.author
        return super().save(commit=True)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ['content_comment', 'to_post', ]

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('instance')
        super(AddCommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.author = self.author
        return super().save(commit=True)
