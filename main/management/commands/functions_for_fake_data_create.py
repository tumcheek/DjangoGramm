import random

from .factories import *
from ...models import *
from cloudinary import uploader
from faker import Faker


def delete_all_data():
    UserModel.objects.all().delete()
    FollowerFollowingModel.objects.all().delete()
    MediaTypeModel.objects.all().delete()
    MediaModel.objects.all().delete()
    PostModel.objects.all().delete()
    LikeModel.objects.all().delete()
    TagModel.objects.all().delete()
    BookmarksModel.objects.all().delete()


def create_fake_users(num_users):
    people = []
    for _ in range(num_users):
        person = UserFactory(is_verify=True)
        people.append(person)
    return people


def create_fake_follower_following(num_follower_following, people):
    for _ in range(num_follower_following):
        FollowerFollowingFactory(followers=random.choice(people), following=random.choice(people))


def create_fake_media_types(types):
    media_types = []
    for _type in types:
        media_type = MediaTypeFactory(name=_type)
        media_types.append(media_type)
    return media_types


def create_fake_medias(num_media, media_types):
    medias = []
    for _ in range(num_media):
        media = MediaFactory(
            media_type=random.choice(media_types),
            media_src=uploader.upload(Faker().image(), folder='posts_media/')['url'])
        medias.append(media)
    return medias


def create_fake_posts(num_posts, people, medias):
    posts = []
    for _ in range(num_posts):
        post = PostFactory(user=random.choice(people))
        current_media = random.choices(medias, k=8)
        post.medias.add(*current_media)
        posts.append(post)
    return posts


def create_fake_likes(num_likes, people, posts):
    for _ in range(num_likes):
        LikeFactory(user=random.choice(people), post=random.choice(posts))


def create_fake_bookmarks(num_bookmarks, people, posts):
    for _ in range(num_bookmarks):
        BookmarksFactory(user=random.choice(people), post=random.choice(posts))


def create_fake_tags(num_tags, posts, people):
    for _ in range(num_tags):
        tag = TagFactory()
        tag.post.add(*random.choices(posts, k=8))
        tag.user.add(*random.choices(people, k=8))

