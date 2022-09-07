from .models import TagModel


def get_user_posts_info(posts_query, user, post_creator):
    posts = []
    for post in posts_query:
        all_post_media = []
        all_post_tags = []
        for media in post.medias.all():
            all_post_media.append(media.media_src)
        for tag in TagModel.objects.filter(post=post.pk):
            all_post_tags.append(tag.name)

        post_info = {
            'post_creator': post_creator.username,
            'post_creator_avatar': post_creator.avatar_src,
            'post_content': post.content,
            'created_at': post.created_at,
            'post_pk': post.pk,
            'media': all_post_media,
            'tags': all_post_tags,
            'likes': post.likemodel_set.all().count(),
            'is_liked': True if post.likemodel_set.filter(user_id=user.pk) else False,
            'is_bookmark': False if post.bookmarksmodel_set.filter(user_id=user.pk) else True

        }

        posts.append(post_info)

    return posts


def get_post_info(post, user, post_creator):
    all_post_media = []
    all_post_tags = []
    for media in post.medias.all():
        all_post_media.append(media.media_src)
    for tag in TagModel.objects.filter(post=post.pk):
        all_post_tags.append(tag.name)
    post_info = {
        'post_creator': post_creator.username,
        'post_creator_avatar': post_creator.avatar_src,
        'post_content': post.content,
        'created_at': post.created_at,
        'post_pk': post.pk,
        'media': all_post_media,
        'tags': all_post_tags,
        'likes': post.likemodel_set.all().count(),
        'is_liked': True if post.likemodel_set.filter(user_id=user.pk) else False,
        'is_bookmark': False if post.bookmarksmodel_set.filter(user_id=user.pk) else True

    }

    return post_info


def add_tags_post(post_tags_list, user, post):
    for post_tag in post_tags_list:
        tag = TagModel.objects.create(name=post_tag[1:]) if post_tag[0] == '#' \
            else TagModel.objects.create(name=post_tag)
        tag.user.add(user)
        tag.post.add(post)
        tag.save()
