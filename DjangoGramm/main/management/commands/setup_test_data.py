import random

from django.db import transaction
from django.core.management.base import BaseCommand

from main.models import UserModel, MediaTypeModel, FollowerFollowingModel, MediaModel, PostModel,\
    LikeModel, TagModel, BookmarksModel
from main.factories import UserFactory, FollowerFollowingFactory, MediaTypeFactory, MediaFactory, \
    PostFactory, LikeFactory, TagFactory, BookmarksFactory


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
        media_types = []
        medias = []
        posts = []

        for _ in range(50):
            person = UserFactory()
            people.append(person)

        for _ in range(5):
            following_followers = FollowerFollowingFactory()
            follower = random.choices(people, k=8)
            following = random.choices(people, k=8)
            following_followers.follower.add(*follower)
            following_followers.following.add(*following)

        for _ in range(3):
            media_type = MediaTypeFactory()
            media_types.append(media_type)

        for _ in range(5):
            media = MediaFactory()
            medias.append(media)

        for _ in range(15):
            post = PostFactory()
            current_media = random.choices(medias, k=8)
            post.medias.add(*current_media)
            posts.append(post)

        for _ in range(50):
            users = random.choices(people, k=8)
            current_post = random.choices(posts, k=8)
            LikeFactory()
            tag = TagFactory()
            tag.post.add(*current_post)
            tag.user.add(*users)
            BookmarksFactory()



