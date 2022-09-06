from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.views import generic, View
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout
from .forms import SignupForm
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from .utils import send_email_for_verify, get_post_info, get_user_posts_info, add_tags_post
from pathlib import Path
from .models import *
from django.contrib.auth.views import LoginView as Login

User = get_user_model()


def login_redirect_view(request):
    username = request.user.username
    return redirect(reverse('main:profile', kwargs={'username': username}))


class ProfileView(View):
    template_name = 'main/profile/profile.html'

    def get(self, request, username):
        try:
            if not request.user.is_verify:
                return redirect('main:confirm_error')
        except AttributeError:
            return redirect('main:login')
        if not request.user.is_authenticated:
            return redirect('main:login')

        login_user_username = request.user.username
        user = request.user if username == login_user_username else User.objects.get(username=username)
        followers_count = user.followers.all().count()
        following_count = user.following.all().count()
        posts = get_user_posts_info(user.postmodel_set.all().order_by('-created_at'), request.user, user)
        is_my_profile = True if username == login_user_username else False
        is_follow = True if FollowerFollowingModel.objects\
            .filter(followers=User.objects.get(username=username), following=request.user) else False
        context = {
            'user': user,
            'avatar_src': Path(str(user.avatar_src)),
            'followers_count': followers_count,
            'following_count': following_count,
            'posts': posts,
            'is_my_profile': is_my_profile,
            'login_user_username': login_user_username,
            'is_follow': is_follow
            }
        return render(request, self.template_name, context)


class ProfileSettingView(View):
    template_name = 'main/profile/profile_settings.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('main:login')
        context = {
            'username': request.user.username
        }

        return render(request, self.template_name, context)

    @staticmethod
    def post(request):
        form = request.POST
        user = request.user
        uploaded_avatar = request.FILES.get('avatar')
        if uploaded_avatar:
            user.avatar_src = uploaded_avatar
        user.first_name = form['first_name']
        user.last_name = form['last_name']
        user.bio = form['bio']
        user.save()
        return redirect(reverse('main:profile', kwargs={'username': request.user.username}))


class LoginView(Login):
    template_name = 'main/registration/login.html'
    redirect_authenticated_user = True


class EmailVerifyView(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is None or not token_generator.check_token(user, token):
            return HttpResponse('Error! Invalid link.')
        user.is_verify = True
        user.save()
        login(request, user)
        return redirect('main:profile_setting')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                User.DoesNotExist,
                ValidationError,
        ):
            user = None
        return user


class RegistrationView(View):
    template_name = 'main/registration/register.html'

    def get(self, request):
        context = {
            'form': SignupForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('main:confirm_email')
        context = {
            'form': form
        }

        return render(request, self.template_name, context)


class LikeView(View):
    @staticmethod
    def post(request, pk):
        post = get_object_or_404(PostModel, id=pk)
        previous_page = request.POST.get('next', '/')

        if post.likemodel_set.filter(user_id=request.user.pk):
            post.likemodel_set.filter(user_id=request.user.pk).delete()
        else:
            post_like = LikeModel(post=post, user=request.user)
            post_like.save()

        return HttpResponseRedirect(previous_page)


class BookmarkView(View):
    @staticmethod
    def post(request, pk):
        post = get_object_or_404(PostModel, id=pk)
        previous_page = request.POST.get('next', '/')
        if post.bookmarksmodel_set.filter(user_id=request.user.pk):
            post.bookmarksmodel_set.filter(user_id=request.user.pk).delete()
        else:
            post_bookmark = BookmarksModel(post=post, user=request.user)
            post_bookmark.save()
        return HttpResponseRedirect(previous_page)


class NewPostView(View):
    @staticmethod
    def post(request):
        form = request.POST
        upload_media = request.FILES.getlist('media')
        user = request.user
        new_post = PostModel(user=user, content=form['content'])
        new_post.save()
        for media in upload_media:
            media_type = MediaTypeModel.objects.get(name=media.content_type[media.content_type.find('/') + 1:])
            post_media = MediaModel(media_src=media, media_type_id=media_type.pk)
            post_media.save()
            new_post.medias.add(post_media)
            new_post.save()
        post_tags_list = form['tags'].split()
        add_tags_post(post_tags_list, user, new_post)

        return redirect(reverse('main:profile', kwargs={'username': request.user.username}))


class FeedView(View):
    template_name = 'main/profile/feed.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('main:login')
        user = request.user
        all_following = user.following.all()
        posts = []

        for following in all_following:
            user_posts = PostModel.objects\
                .filter(user_id=following.followers_id)\
                .order_by('-created_at')
            for user_post in user_posts:
                posts.append(get_post_info(user_post, user, User.objects.get(pk=following.followers_id)))
        context = {
            'user': request.user.username,
            'posts': sorted(posts, key=lambda x: x['created_at'], reverse=True)
            }
        return render(request, self.template_name, context)


class FollowersFollowingView(View):
    template_name = 'main/profile/follower_following.html'

    def get(self, request, username, followers_following):
        if not request.user.is_authenticated:
            return redirect('main:login')
        current_user_page = User.objects.get(username=username)
        login_user_username = request.user.username
        user_list = []
        if followers_following == 'followers':
            user_follower_following = current_user_page.followers.all()
            for user in user_follower_following:
                user_list.append(User.objects.get(pk=user.following_id))
        else:
            user_follower_following = current_user_page.following.all()
            for user in user_follower_following:
                user_list.append(User.objects.get(pk=user.followers_id))

        context = {
            'user_list': user_list,
            'follower_following': followers_following,
            'login_user_username': login_user_username
        }
        return render(request, self.template_name, context)


def add_new_tags_view(request, pk):
    if request.method == "POST":
        tag_list = request.POST['tags'].split()
        post = PostModel.objects.get(pk=pk)
        add_tags_post(tag_list, request.user, post)
        return redirect(reverse('main:profile', kwargs={'username': request.user.username}))


def follow_user_view(request, username):
    if request.method == "POST":
        if request.user.following.filter(followers_id=User.objects.get(username=username).pk):
            request.user.following.filter(followers_id=User.objects.get(username=username).pk).delete()
        else:
            pass
            FollowerFollowingModel.objects.create(followers=User.objects.get(username=username), following=request.user)
        return redirect(reverse('main:profile', kwargs={'username': username}))

