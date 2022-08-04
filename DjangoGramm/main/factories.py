# from django_faker import Faker
import factory
from factory.django import DjangoModelFactory
from .m]


class UserFactory(factory.Factory):
    class Meta:
        model = UserModel

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    bio = factory.Faker('last_name')
    avatar_src = factory.Faker('last_name')
    title = factory.Faker('sentence', nb_words=4)
    author_name = factory.Faker('name')

