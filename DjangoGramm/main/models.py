from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

from django.conf import settings


class UserModel(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=250)
    avatar_src = CloudinaryField(
        folder=getattr(settings, 'CLOUDINARY_AVATAR_FOLDER'),
        default=getattr(settings, 'CLOUDINARY_DEFAULT_IMG'))
    is_verify = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['usernames']


class FollowerFollowingModel(models.Model):
    followers = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['followers', 'following'],  name="unique_followers")
        ]


class MediaTypeModel(models.Model):
    name = models.CharField(max_length=10)


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MediaModel(TimeStampMixin):
    media_type = models.ForeignKey(MediaTypeModel, on_delete=models.CASCADE)
    media_src = CloudinaryField('image', folder=getattr(settings, 'CLOUDINARY_MEDIA_FOLDER'))


class PostModel(TimeStampMixin):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    medias = models.ManyToManyField(MediaModel)
    content = models.TextField()


class LikeModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)


class TagModel(models.Model):
    name = models.CharField(max_length=120)
    post = models.ManyToManyField(PostModel)
    user = models.ManyToManyField(UserModel)


class BookmarksModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

