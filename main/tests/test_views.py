from cloudinary import uploader
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from pathlib import Path

from social_django.models import UserSocialAuth

from ..models import *
from ..views import ProfileView


class BaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(
            username='test',
            email='test@test.com',
            password='PassE228',
            is_verify=True

        )
        self.user_password = 'PassE228'
        self.social_user = UserSocialAuth.objects.create(
            user=self.user,
            provider='google-oauth2',
        )
        self.post = PostModel.objects.create(
            user=self.user,
            content='Test'
        )

        self.register_url = 'main:register'
        self.login_redirect_url = 'main:login_redirect'
        self.login_url = 'main:login'
        self.profile_url = 'main:profile'
        self.settings_url = 'main:profile_setting'
        self.feed_url = 'main:feed'
        self.followers_following_url = 'main:followers_following'
        self.verify_email_url = 'main:verify_email'
        self.like_url = '/djangogramm/like/'
        self.bookmark_url = '/djangogramm/bookmark/'
        self.new_post_url = 'main:new_post'
        self.new_tags_url = '/djangogramm/new_tags/'
        self.follow_user_url = 'main:follow_user'
        self.social_login_complete = 'social:complete'

        self.img = Path(__file__).resolve().parent / 'test_media' / 'test.jpg'
        self.media_type = MediaTypeModel.objects.create(name='jpg')
        self.followers_following_dict = {
            'username': self.user.username,
            'followers_following': 'follower'
        }
        self.register_info = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password1': 'PassE228',
            'password2': 'PassE228',

        }
        self.user_data = {
            'username': self.user.email,
            'password': self.user_password

        }
        self.settings_data = {
            'first_name': 'Jody',
            'last_name': 'Smith',
            'bio': 'Test'
        }

        return super().setUp()


class RegistrationView(BaseTest):
    def test_register_GET(self):
        response = self.client.get(reverse(self.register_url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/registration/register.html')

    def test_register_POST(self):
        response = self.client.post(reverse(self.register_url), data=self.register_info)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'main/registration/verify_email.html')


class LoginRedirectTest(BaseTest):
    def test_login_redirect(self):
        self.client.post(reverse(self.login_url), data=self.user_data, format='text/html')
        response = self.client.get(reverse(self.login_redirect_url))
        self.assertEqual(response.status_code, 302)


class ProfileTest(BaseTest):
    def test_profile(self):
        self.client.post(reverse(self.login_url), data=self.user_data, format='text/html')
        response = self.client.get(reverse(self.profile_url, kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile/profile.html')

    def test_social_profile(self):
        self.user.is_verify = False
        self.user.save()
        request = self.factory.get(reverse(self.social_login_complete, kwargs={'backend': 'google-oauth2'}))
        request.user = self.user
        request.user.social_auth.set([self.social_user])
        response = ProfileView.as_view()(request, request.user.username)
        self.assertEqual(response.url, reverse(self.settings_url))


class ProfileSettingTest(BaseTest):
    def test_settings_GET(self):
        self.client.post(reverse(self.login_url), data=self.user_data, format='text/html')
        response = self.client.get(reverse(self.settings_url))
        self.assertEqual(response.status_code, 200)

    def test_settings_POST(self):
        self.client.post(reverse(self.login_url), data=self.user_data, format='text/html')
        response = self.client.post(reverse(self.settings_url), self.settings_data)
        self.assertEqual(response.status_code, 302)


class LoginTest(BaseTest):
    def test_login_GET(self):
        response = self.client.get(reverse(self.login_url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/registration/login.html')

    def test_login_POST(self):
        self.client.post(reverse(self.register_url), self.register_info)
        response = self.client.post(reverse(self.login_url),
                                    data={'username': self.user.email, 'password': self.user_password},
                                    format='text/html')
        self.assertEqual(response.status_code, 302)


class EmailVerify(BaseTest):
    def test_verify_email_exist_user(self):
        user = UserModel.objects.create_user('testuser', 'crytest@gmail.com')
        user.set_password('tetetebvghhhhj')
        user.is_verify = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        response = self.client.get(reverse(self.verify_email_url, kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 302)
        user = UserModel.objects.get(email='crytest@gmail.com')
        self.assertTrue(user.is_verify)

    def test_verify_email_no_exist_user(self):
        user = UserModel.objects.create_user('testuser', 'crytest@gmail.com')
        user.set_password('tetetebvghhhhj')
        user.is_verify = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk + 1))
        token = token_generator.make_token(user)
        response = self.client.get(reverse(self.verify_email_url, kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 200)


class LikeTest(BaseTest):
    def test_add_like(self):
        self.client.post(reverse(self.login_url), data=self.user_data, format='text/html')
        response = self.client.post(self.like_url, {'pk': self.post.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.likemodel_set.all().count(), 1)

    def test_delete_like(self):
        self.client.post(reverse(self.login_url), data=self.user_data,
                         format='text/html')
        self.client.post(self.like_url, {'pk': self.post.pk})
        response = self.client.post(self.like_url, {'pk': self.post.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.likemodel_set.all().count(), 0)


class BookmarkTest(BaseTest):
    def test_add_bookmark(self):
        self.client.post(reverse(self.login_url), data=self.user_data, format='text/html')
        response = self.client.post(self.bookmark_url, {'pk': self.post.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.bookmarksmodel_set.all().count(), 1)

    def test_delete_bookmark(self):
        self.client.post(reverse(self.login_url), data=self.user_data, format='text/html')
        self.client.post(self.bookmark_url, {'pk': self.post.pk})
        response = self.client.post(self.bookmark_url, {'pk': self.post.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.bookmarksmodel_set.all().count(), 0)


class AddNewPostTest(BaseTest):
    def test_add_new_post(self):
        media = uploader.upload(self.img)
        self.client.post(reverse(self.login_url), data=self.user_data, format='text/html')

        response = self.client.post(reverse(self.new_post_url), data={'content': 'test', 'media': [media],
                                                                      'tags': 'test'})
        self.assertEqual(response.status_code, 302)


class FeedTest(BaseTest):
    def test_feed(self):
        self.client.post(reverse(self.login_url), data=self.user_data, format='text/html')
        response = self.client.get(reverse(self.feed_url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile/feed.html')


class FollowersFollowing(BaseTest):
    def test_followers_following(self):
        self.client.post(reverse(self.login_url), data=self.user_data, format='text/html')
        response = self.client.get(reverse(self.followers_following_url, kwargs=self.followers_following_dict))
        self.assertEqual(response.status_code, 200)


class AddNewTagsTest(BaseTest):
    def test_add_new_tag(self):
        self.client.post(reverse(self.login_url), data=self.user_data, format='text/html')
        response = self.client.post(self.new_tags_url, {'pk': self.post.pk, 'tags': ['test']})
        self.assertEqual(response.status_code, 200)


class FollowUserTest(BaseTest):
    def test_follow_user(self):
        user_to_follow = UserModel.objects.create_user(
            username='test_follow',
            email='follow@follow.com',
            password='PassE228',
            is_verify=True
        )
        self.client.post(reverse(self.login_url), data=self.user_data, format='text/html')
        response = self.client.post(reverse(self.follow_user_url, args=[user_to_follow.username]))
        self.assertEqual(response.status_code, 302)
