from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from .models import TagModel


def send_email_for_verify(request, user):
    current_site = get_current_site(request)

    context = {
        "user": user,
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": token_generator.make_token(user),

    }
    message = render_to_string(
        'main/registration/verify_email.html',
        context=context
    )
    email = EmailMessage(
        'Verify email',
        message,
        to=[user.email]
    )
    email.send()


def get_posts_list(posts_query, request):
    posts = []

    for post in posts_query:
        post_info = []
        all_post_media = []
        all_post_tags = []
        post_info.append(post.content)
        for media in post.medias.all():
            all_post_media.append(media.media_src)
        post_info.append(all_post_media)
        for tag in TagModel.objects.filter(post=post.pk):
            all_post_tags.append(tag.name)
        post_info.append(all_post_tags)
        likes = post.likemodel_set.all().count()
        post_info.append(likes)
        post_info.append(post.pk)
        is_liked = True if post.likemodel_set.filter(user_id=request.user.pk) else False
        post_info.append(is_liked)
        is_bookmark = False if post.bookmarksmodel_set.filter(user_id=request.user.pk) else True
        post_info.append(is_bookmark)
        posts.append(post_info)

    return posts
