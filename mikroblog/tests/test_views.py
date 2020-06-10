from django.contrib.auth import authenticate, login
from django.http import request
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils.encoding import force_text

from mikroblog.models import Post, Comment, TalkAbout, get_posts_on_specific_tag
from accounts.models import CustomUser
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.index_url = reverse('index')
        self.test_user = CustomUser.objects.create(username='test_user')
        self.test_user.set_password('test')
        self.test_user.save()
        self.client.force_login(self.test_user)

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mikroblog/index.html')

    def test_index_POST_adds_new_post(self):
        response = self.client.post(self.index_url, {
            'author': self.test_user,
            'content_post': 'test_content'
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Post.objects.first().content_post, 'test_content')

    def test_index_POST_adds_new_post_no_data(self):
        response = self.client.post(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Post.objects.count(), 0)

    def test_index_POST_adds_new_comment(self):
        self.post = Post.objects.create(
            author=self.test_user,
            content_post='test_content'
        )
        response = self.client.post(self.index_url, {
            'author': self.test_user,
            'content_comment': 'test_content',
            'to_post': self.post.id
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Comment.objects.first().to_post, self.post)

    def test_index_POST_adds_new_comment_no_data(self):
        response = self.client.post(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Comment.objects.count(), 0)

    def test_delete_post(self):
        self.post = Post.objects.create(
            author=self.test_user,
            content_post='test_content'
        )

        response = self.client.delete(reverse('delete', args=[1]))

        self.assertEquals(response.status_code, 302)
        self.assertIs(Post.objects.count(), 0)
        self.assertRedirects(response, '/')

    def test_tag_view_GET(self):
        response = self.client.get(reverse('tag', args=['#test_tag']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mikroblog/tag.html')
        self.assertEquals(response.context['actual_tag'], '#test_tag')

    def test_profile_view_GET(self):
        response = self.client.get(reverse('profile', args=[self.test_user.username]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mikroblog/profile.html')

    def test_profile_view_user_non_exist_GET(self):
        response = self.client.get(reverse('profile', args=['non_exist_user']))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_post_view_GET(self):
        self.post = Post.objects.create(
            author=self.test_user,
            content_post='test_content'
        )

        response = self.client.get(reverse('post', args=[self.post.id]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mikroblog/post_details.html')

    def test_post_view_non_exist_GET(self):
        response = self.client.get(reverse('post', args=[2]))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_edit_post_view_GET(self):
        self.post = Post.objects.create(
            author=self.test_user,
            content_post='test_content'
        )

        response = self.client.get(reverse('edit', args=[self.post.id]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mikroblog/post_edit_form.html')
        self.assertEquals(response.context['post'], self.post)

    def test_post_like_toggle_POST(self):
        self.post = Post.objects.create(
            author=self.test_user,
            content_post='test_content'
        )

        response = self.client.post(reverse('post_like_toggle'), {'post_id': self.post.id},
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

        self.assertJSONEqual(response.content, {'liked': False, 'numOfLikes': 1})

    def test_check_notifications(self):
        self.post = Post.objects.create(
            author=self.test_user,
            content_post='test_content'
        )

        TalkAbout.objects.create(_from=self.test_user, to=self.test_user, where=self.post)
        response = self.client.get(reverse('check_notifications'))
        self.assertJSONEqual(response.content, {'notifications': [{'from': 'test_user', 'id': 1,
                                                                   'to': 'test_user', 'where': 1}]})

    def test_delete_notification(self):
        self.post = Post.objects.create(
            author=self.test_user,
            content_post='test_content'
        )

        TalkAbout.objects.create(_from=self.test_user, to=self.test_user, where=self.post)
        response = self.client.delete(reverse('delete_notification', args=[1]))

        self.assertEquals(TalkAbout.objects.count(), 0)
        self.assertEquals(response.status_code, 302)

    def test_block_user(self):
        response = self.client.get(reverse('block_user', args=[1]))

        self.assertIsNotNone(self.test_user.blocked.first())
        self.assertEquals(response.status_code, 302)

    def test_check_blacklist(self):
        self.test_user.blocked.add(self.test_user)

        response = self.client.get(reverse('check_blacklist'))

        self.assertJSONEqual(response.content, {'blackList': [{'blocked': 'test_user', 'id': 1}]})

    def test_remove_from_blacklist(self):
        self.test_user.blocked.add(self.test_user)

        response = self.client.delete(reverse('remove_from_blacklist', args=[1]), {'id': self.test_user.id})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.test_user.blocked.first(), None)

    def test_edit_post_view_POST(self):
        self.post = Post.objects.create(
            author=self.test_user,
            content_post='test_content'
        )

        response = self.client.post(reverse('edit', args=[self.post.id]), {
            'content_post': 'new_content_post'
        })
        self.post.refresh_from_db()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.post.content_post, 'new_content_post')
