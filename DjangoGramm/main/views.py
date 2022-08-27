from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.views import generic, View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout
from .forms import SignupForm
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from .utils import send_email_for_verify, get_posts_list
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from .models import *
from django.contrib.auth.views import LoginView as Login

User = get_user_model()


class ProfileView(View):
    template_name = 'main/profile/profile.html'

    def get(self, request):
        try:
            if not request.user.is_verify:
                return redirect('main:confirm_error')
        except AttributeError:
            return redirect('main:login')
        if request.user.is_authenticated:
            user = request.user
            posts = get_posts_list(user.postmodel_set.all().order_by('-created_at'), request)
            context = {
                'user': user,
                'avatar_src': Path(str(user.avatar_src)),
                'posts': posts,
            }
            return render(request, self.template_name, context)

        return redirect('main:login')


class ProfileSettingView(View):
    template_name = 'main/profile/profile_settings.html'

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return HttpResponse('You must login!')

    def post(self, request):
        form = request.POST
        uploaded_avatar = request.FILES.get('avatar')
        user = request.user
        if uploaded_avatar:
            user.avatar_src = uploaded_avatar
        user.first_name = form['first_name']
        user.last_name = form['last_name']
        user.bio = form['bio']
        user.save()
        return redirect('main:profile')


class LoginView(Login):
    template_name = 'main/registration/login.html'
    redirect_authenticated_user = True


class EmailVerifyView(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
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
    def post(self, request, pk):
        post = get_object_or_404(PostModel, id=pk)

        if post.likemodel_set.filter(user_id=request.user.pk):
            post.likemodel_set.filter(user_id=request.user.pk).delete()
        else:
            post_like = LikeModel(post=post, user=request.user)
            post_like.save()
        return redirect('main:profile')


class BookmarkView(View):
    def post(self, request, pk):
        post = get_object_or_404(PostModel, id=pk)
        if post.bookmarksmodel_set.filter(user_id=request.user.pk):
            post.bookmarksmodel_set.filter(user_id=request.user.pk).delete()
        else:
            post_bookmark = BookmarksModel(post=post, user=request.user)
            post_bookmark.save()
        return redirect('main:profile')




