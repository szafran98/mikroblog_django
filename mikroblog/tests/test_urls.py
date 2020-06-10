from django.test import SimpleTestCase
from django.urls import reverse, resolve
from mikroblog.views import *


class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_tag_url_is_resolved(self):
        url = reverse('tag', args=['#testtag'])
        self.assertEqual(resolve(url).func, tag_view)

    def test_post_url_is_resolved(self):
        url = reverse('post', args=['13'])
        self.assertEqual(resolve(url).func, post_view)

    def test_profile_url_is_resolved(self):
        url = reverse('profile', args=['testuser'])
        self.assertEqual(resolve(url).func, profile_view)

    def test_delete_url_is_resolved(self):
        url = reverse('delete', args=['13'])
        self.assertEqual(resolve(url).func, delete_post)

    def test_edit_url_is_resolved(self):
        url = reverse('edit', args=['13'])
        self.assertEqual(resolve(url).func, edit_post)

    def test_like_url_is_resolved(self):
        url = reverse('post_like_toggle')
        self.assertEqual(resolve(url).func, post_like_toggle)

    def test_delete_notification_url_is_resolved(self):
        url = reverse('delete_notification', args=['13'])
        self.assertEqual(resolve(url).func, delete_notification)

    def test_notifications_url_is_resolved(self):
        url = reverse('check_notifications')
        self.assertEqual(resolve(url).func, check_notifications)

    def test_blacklist_url_is_resolved(self):
        url = reverse('check_blacklist')
        self.assertEqual(resolve(url).func, check_blacklist)

    def test_block_user_url_is_resolved(self):
        url = reverse('block_user', args=['13'])
        self.assertEqual(resolve(url).func, block_user)

    def test_remove_from_blacklist_url_is_resolved(self):
        url = reverse('remove_from_blacklist', args=['13'])
        self.assertEqual(resolve(url).func, remove_from_blacklist)
