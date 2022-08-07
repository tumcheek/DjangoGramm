import factory
from factory.django import DjangoModelFactory
from .models import UserModel, MediaTypeModel, FollowerFollowingModel, MediaModel, PostModel,\
    LikeModel, TagModel, BookmarksModel


class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    bio = factory.Faker('sentence', nb_words=5)
    avatar_src = factory.Faker('url')


class FollowerFollowingFactory(DjangoModelFactory):
    class Meta:
        model = FollowerFollowingModel


class MediaTypeFactory(DjangoModelFactory):
    class Meta:
        model = MediaTypeModel
    name = factory.Faker('word')


class MediaFactory(DjangoModelFactory):
    class Meta:
        model = MediaModel

    media_type = factory.SubFactory(MediaTypeFactory)
    media_src = factory.Faker('url')


class PostFactory(DjangoModelFactory):
    class Meta:
        model = PostModel

    user = factory.SubFactory(UserFactory)
    content = factory.Faker('sentence', nb_words=30)


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = LikeModel

    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
    likes = factory.Faker('random_int')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = TagModel

    name = factory.Faker('sentence', nb_words=5)


class BookmarksFactory(DjangoModelFactory):
    class Meta:
        model = BookmarksModel
