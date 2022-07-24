from django.db import models
from django.core.mail import send_mail


class User(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    bio = models.CharField(max_length=250)
    avatar = models.CharField(max_length=120)

    def create_unique_link(self):
        return f'django-gram/activate/{User.pk}'

    def send_unique_link(self):

        send_mail(
            subject='Activation',
            message=self.create_unique_link(),
            from_email='from@example.com',
            recipient_list=[self.email],
            fail_silently=False,
        )

    def create_user(self, email):
        self.email = email
        self.send_unique_link()

    def set_user(self, first_name, last_name, bio, avatar):
        self.first_name = first_name
        self.last_name = last_name
        self.bio = bio
        self.avatar = avatar

    def get_user(self):
        return self.email, self.first_name, self.last_name, self.bio, self.avatar


class FollowerFollowing(models.Model):
    follower_id = User()
    following_id = User()


class MediaType(models.Model):
    name = models.CharField(max_length=10)


class Media(models.Model):
    media_type_id = models.ForeignKey(MediaType)
    media_src = models.CharField(max_length=100)


class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ManyToManyField(Media)
    create_at = models.DateTimeField('date published')

    def create_post(self, user_id, content):
        self.user_id = user_id
        self.content = content


class Base(models.Model):
    post_id = models.ManyToManyField(Post)
    user_id = models.ManyToManyField(User)


class Like(Base):
    likes = models.IntegerField(default=0)


class Tag(Base):
    tag = models.CharField(max_length=50)


class Bookmarks(Base):
    is_bookmark = models.BooleanField(default=False)

