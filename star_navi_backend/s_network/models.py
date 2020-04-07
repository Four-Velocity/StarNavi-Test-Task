from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    company = models.CharField(max_length=80, blank=True)
    role = models.CharField(max_length=80, blank=True)

    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)

    bio = models.TextField(blank=True)

    avatar = models.ImageField('photo', upload_to='avatars', blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.owner.username}\'s profile'

    def liked_posts(self):
        likes = self.likes.all()
        posts_pk = [like.post.pk for like in likes]
        return posts_pk


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    pub_date = models.DateTimeField('dateTime published', auto_now_add=True)
    image = models.ImageField(upload_to='posts', blank=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f'Post #{self.pk}, {self.title}, by: {self.creator.email}'


class Like(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='likes_list')
    user = models.ManyToManyField(User, related_name="likes", blank=True)

    def __str__(self):
        return f'Likes for Post #{self.post.pk}'
