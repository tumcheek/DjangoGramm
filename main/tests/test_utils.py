from django.test import TestCase, Client
from django.urls import reverse
from ..models import *
from ..utils import get_post_info
from pathlib import Path
from cloudinary import uploader, CloudinaryResource


class UtilsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='test',
            email='test@test.com',
            password='PassE228',
            is_verify=True

        )
        self.user_password = 'PassE228'
        self.media_type = MediaTypeModel.objects.create(name='jpg')
        self.tags = TagModel.objects.create(name='test')
        self.img = Path(__file__).resolve().parent / 'test_media' / 'test.jpg'
        self.data = uploader.upload(self.img,  folder='posts_media/')['url']
        self.media = MediaModel.objects.create(
            media_src=self.data,
            media_type=self.media_type
        )
        self.post = PostModel.objects.create(
            user=self.user,
            content='Test'
        )
        self.tags.post.add(self.post)
        self.tags.save()
        self.post.medias.add(self.media)
        self.post.save()
        self.login_url = 'main:login'
        self.result = {
            'post_creator': self.user.username,
            'post_creator_avatar': self.user.avatar_src,
            'post_content': self.post.content,
            'created_at': self.post.created_at,
            'post_pk': self.post.pk,
            'media': [self.media.media_src[:self.media.media_src.find('.jpg')]],
            'tags': ['test'],
            'likes': self.post.likemodel_set.all().count(),
            'is_liked': True if self.post.likemodel_set.filter(user_id=self.user.pk) else False,
            'is_bookmark': False if self.post.bookmarksmodel_set.filter(user_id=self.user.pk) else True
        }

    def test_get_post_info(self):
        self.client.post(reverse(self.login_url), data={'username': self.user.email, 'password': self.user_password},
                         format='text/html')
        result = get_post_info(self.post, self.user, self.user)
        self.assertEqual(result['media'], self.result['media'])
