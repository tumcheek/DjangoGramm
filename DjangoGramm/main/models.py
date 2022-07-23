from django.db import models
from django.core.mail import send_mail


class User(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    bio = models.CharField(max_length=250)
    avatar = models.CharField(max_length=120)

    def create_unique_link(self, user_id):
        return f'django-gram/activate/{user_id}'

    def send_unique_link(self, user_id):

        send_mail(
            subject='Activation',
            message=self.create_unique_link(user_id),
            from_email='from@example.com',
            recipient_list=[self.email],
            fail_silently=False,
        )

    def create_user(self, email, user_id):
        self.email = email
        self.send_unique_link(user_id)

    def set_user(self, first_name, last_name, bio, avatar):
        self.first_name = first_name
        self.last_name = last_name
        self.bio = bio
        self.avatar = avatar

    def get_user(self):
        return self.email, self.first_name, self.last_name, self.bio, self.avatar

