from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from django.views import generic, View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from .forms import SignupForm
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from .utils import send_email_for_verify

User = get_user_model()


class EmailVerifyView(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.is_verify = True
            user.save()
            login(request, user)
            return redirect('main:register')


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

