from django.db import models


class UserModel(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    bio = models.CharField(max_length=250)
    avatar_src = models.CharField(max_length=120)


class FollowerFollowingModel(models.Model):
    follower = models.ManyToManyField(UserModel, related_name='follower')
    following = models.ManyToManyField(UserModel, related_name='following')


class MediaTypeModel(models.Model):
    name = models.CharField(max_length=10)


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MediaModel(TimeStampMixin):
    media_type = models.ForeignKey(MediaTypeModel, on_delete=models.CASCADE)
    media_src = models.CharField(max_length=100)


class PostModel(TimeStampMixin):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    medias = models.ManyToManyField(MediaModel)
    content = models.TextField()


class LikeModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)


class TagModel(models.Model):
    name = models.CharField(max_length=120)
    post = models.ManyToManyField(PostModel)
    user = models.ManyToManyField(UserModel)


class BookmarksModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_bookmark = models.BooleanField(default=False)

