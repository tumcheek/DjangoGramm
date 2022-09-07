from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

from ..views import *
from ..registration_view import RegistrationView


class TestUrls(SimpleTestCase):
    def test_new_tags_url_is_resolved(self):
        url = reverse('main:new_tags', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, add_new_tags_view)

    def test_login_redirect_url_is_resolved(self):
        url = reverse('main:login_redirect')
        self.assertEqual(resolve(url).func, login_redirect_view)

    def test_logout_url_is_resolved(self):
        url = reverse('main:logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_login_url_is_resolved(self):
        url = reverse('main:login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_confirm_email_url_is_resolved(self):
        url = reverse('main:confirm_email')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_verify_email_url_is_resolved(self):
        url = reverse('main:verify_email', kwargs={'uidb64': 'test', 'token': 'test'})
        self.assertEqual(resolve(url).func.view_class, EmailVerifyView)

    def test_confirm_error_url_is_resolved(self):
        url = reverse('main:confirm_error')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_register_url_is_resolved(self):
        url = reverse('main:register')
        self.assertEqual(resolve(url).func.view_class, RegistrationView)

    def test_feed_url_is_resolved(self):
        url = reverse('main:feed')
        self.assertEqual(resolve(url).func.view_class, FeedView)

    def test_new_post_url_is_resolved(self):
        url = reverse('main:new_post')
        self.assertEqual(resolve(url).func, add_new_post_view)

    def test_profile_setting_url_is_resolved(self):
        url = reverse('main:profile_setting')
        self.assertEqual(resolve(url).func.view_class, ProfileSettingView)

    def test_profile_url_is_resolved(self):
        url = reverse('main:profile', kwargs={'username': 'test'})
        self.assertEqual(resolve(url).func.view_class, ProfileView)

    def test_follow_user_url_is_resolved(self):
        url = reverse('main:follow_user', kwargs={'username': 'test'})
        self.assertEqual(resolve(url).func, follow_user_view)

    def test_followers_following_url_is_resolved(self):
        url = reverse('main:followers_following', kwargs={'username': 'test', 'followers_following': 'test'})
        self.assertEqual(resolve(url).func.view_class, FollowersFollowingView)

    def test_like_post_url_is_resolved(self):
        url = reverse('main:like_post', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, like_view)

    def test_bookmark_post_url_is_resolved(self):
        url = reverse('main:bookmark_post', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, bookmark_view)

