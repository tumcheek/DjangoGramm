import logging

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as \
    token_generator

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model
from .forms import SignupForm

User = get_user_model()
logger = logging.getLogger(__name__)


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


class RegistrationView(View):
    template_name = 'main/registration/register.html'

    def get(self, request, complete=None):
        if complete == 'complete':
            context = {
                'is_complete': True
            }
        else:
            context = {
                'form': SignupForm(),
                'is_complete': False
            }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password1')
                user = authenticate(email=email, password=password)
                send_email_for_verify(request, user)
                return redirect(reverse('main:register', args=['complete']))
            except User.DoesNotExist:
                logger.debug(User.DoesNotExist)
                return HttpResponse(status=500)
        context = {
            'form': form
        }

        return render(request, self.template_name, context)
