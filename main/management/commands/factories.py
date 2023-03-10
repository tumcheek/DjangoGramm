import factory
from factory.django import DjangoModelFactory
from ...models import UserModel, MediaTypeModel, FollowerFollowingModel, MediaModel, PostModel,\
    LikeModel, TagModel, BookmarksModel


class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel
        django_get_or_create = ('username',)
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    bio = factory.Faker('sentence', nb_words=5)
    is_verify = factory.Faker('pybool')


class FollowerFollowingFactory(DjangoModelFactory):
    class Meta:
        model = FollowerFollowingModel
        django_get_or_create = ('followers', 'following',)

    followers = factory.SubFactory(UserFactory)
    following = factory.SubFactory(UserFactory)


class MediaTypeFactory(DjangoModelFactory):
    class Meta:
        model = MediaTypeModel
    name = factory.Faker('word')


class MediaFactory(DjangoModelFactory):
    class Meta:
        model = MediaModel

    media_type = factory.SubFactory(MediaTypeFactory)
    media_src = factory.django.ImageField()


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


class TagFactory(DjangoModelFactory):
    class Meta:
        model = TagModel

    name = factory.Faker('word')


class BookmarksFactory(DjangoModelFactory):
    class Meta:
        model = BookmarksModel

    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
