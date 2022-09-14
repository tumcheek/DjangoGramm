from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from . import views
from .registration_view import RegistrationView

app_name = 'main'

urlpatterns = [
    path('new_tags/<int:pk>/', views.add_new_tags_view, name='new_tags'),
    path('auth/login-redirect/', views.login_redirect_view, name='login_redirect'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/verify_email/<uidb64>/<token>/', views.EmailVerifyView.as_view(), name='verify_email'),
    path('auth/confirm_email/error/', TemplateView.as_view(template_name='main/registration/confirm_error.html'),
         name='confirm_error'),
    path('auth/registration/<str:complete>', RegistrationView.as_view(), name='register'),
    path('auth/registration/', RegistrationView.as_view(), name='register'),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('new_post/', views.add_new_post_view, name='new_post'),
    path('settings/', views.ProfileSettingView.as_view(), name='profile_setting'),
    path('<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('<str:username>/follow', views.follow_user_view, name='follow_user'),
    path('<str:username>/<str:followers_following>/', views.FollowersFollowingView.as_view(),
         name='followers_following'),
    path('like/<int:pk>', views.like_view, name='like_post'),
    path('bookmark/<int:pk>', views.bookmark_view, name='bookmark_post'),


]

