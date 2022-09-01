import random

from django.db import transaction
from django.core.management.base import BaseCommand

from main.models import UserModel, MediaTypeModel, FollowerFollowingModel, MediaModel, PostModel,\
    LikeModel, TagModel, BookmarksModel
from main.factories import UserFactory, FollowerFollowingFactory, MediaTypeFactory, MediaFactory, \
    PostFactory, LikeFactory, TagFactory, BookmarksFactory

NUM_USERS = 50
NUM_MEDIA = 10
NUM_POSTS = 250
NUM_FOLLOWER_FOLLOWING = 50
MEDIA_TYPE = ['png', 'jpg', 'jpeg']


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        UserModel.objects.all().delete()
        FollowerFollowingModel.objects.all().delete()
        MediaTypeModel.objects.all().delete()
        MediaModel.objects.all().delete()
        PostModel.objects.all().delete()
        LikeModel.objects.all().delete()
        TagModel.objects.all().delete()
        BookmarksModel.objects.all().delete()

        people = []
        medias = []
        posts = []
        media_types = []

        for _ in range(NUM_USERS):
            person = UserFactory(is_verify=True)
            people.append(person)

        for _ in range(NUM_FOLLOWER_FOLLOWING):
            FollowerFollowingFactory(followers=random.choice(people), following=random.choice(people))

        for _type in MEDIA_TYPE:
            media_type = MediaTypeFactory(name=_type)
            media_types.append(media_type)

        for _ in range(NUM_MEDIA):
            media = MediaFactory(media_type=random.choice(media_types))
            medias.append(media)

        for _ in range(NUM_POSTS):
            post = PostFactory(user=random.choice(people))
            current_media = random.choices(medias, k=8)
            post.medias.add(*current_media)
            posts.append(post)

        for _ in range(50):
            users = random.choices(people, k=8)
            current_post = random.choices(posts, k=8)
            LikeFactory(user=random.choice(people), post=random.choice(posts))
            tag = TagFactory()
            tag.post.add(*current_post)
            tag.user.add(*users)
            BookmarksFactory(user=random.choice(people), post=random.choice(posts))



