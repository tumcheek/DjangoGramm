from django.db import transaction
from django.core.management.base import BaseCommand

from .functions_for_fake_data_create import *

NUM_USERS = 200
NUM_MEDIA = 10
NUM_POSTS = 250
NUM_FOLLOWER_FOLLOWING = 1000
NUM_LIKES = 100
NUM_BOOKMARKS = 100
NUM_TAGS = 100
MEDIA_TYPE = ['png', 'jpg', 'jpeg']


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")

        delete_all_data()

        people = create_fake_users(NUM_USERS)
        media_types = create_fake_media_types(MEDIA_TYPE)
        medias = create_fake_medias(NUM_MEDIA, media_types)
        posts = create_fake_posts(NUM_POSTS, people, medias)

        create_fake_follower_following(NUM_FOLLOWER_FOLLOWING, people)
        create_fake_likes(NUM_LIKES, people, posts)
        create_fake_bookmarks(NUM_BOOKMARKS, people, posts)
        create_fake_tags(NUM_TAGS, posts, people)


