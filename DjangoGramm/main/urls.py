from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'main'

urlpatterns = [
    path('confirm_email', TemplateView.as_view(template_name='registration/confirm_email.html'), name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', views.EmailVerifyView.as_view(), name='verify_email'),
    path('registration/', views.RegistrationView.as_view(), name='register'),
]
