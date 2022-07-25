from django.db import models


class UserModel(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    bio = models.CharField(max_length=250)
    avatar_src = models.CharField(max_length=120)


class FollowerFollowingModel(models.Model):
    follower_id = models.ManyToManyField(UserModel, related_name='follower')
    following_id = models.ManyToManyField(UserModel, related_name='following')


class MediaTypeModel(models.Model):
    name = models.CharField(max_length=10)


class MediaModel(models.Model):
    media_type_id = models.ForeignKey(MediaTypeModel, on_delete=models.CASCADE)
    media_src = models.CharField(max_length=100)


class PostModel(models.Model):
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.ManyToManyField(MediaModel)
    create_at = models.DateTimeField('date published')


class BaseModel(models.Model):
    post_id = models.ManyToManyField(PostModel)
    user_id = models.ManyToManyField(UserModel)


class LikeModel(BaseModel):
    likes = models.IntegerField(default=0)


class TagModel(BaseModel):
    tags = models.CharField(max_length=50)


class BookmarksModel(BaseModel):
    is_bookmark = models.BooleanField(default=False)

