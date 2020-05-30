from django import forms
from .models import Post, Comment


class AddPostForm(forms.ModelForm):
    # content_post = forms.TextInput()

    class Meta:
        model = Post

        fields = ('content_post',)


class AddCommentForm(forms.ModelForm):
    # content_comment = forms.TextInput()

    class Meta:
        model = Comment

        fields = ('content_comment', 'to_post',)
