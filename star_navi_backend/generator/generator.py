import datetime as dt
import json
import os
from random import randint, choice
from time import sleep

import requests as r
from faker import Faker

from star_navi_backend.settings import MEDIA_ROOT
from star_navi_backend.utils import get_yaml, hard_get, soft_get
from s_network.models import User, UserProfile, Post, Like
from pytz import timezone


class Generator:
    _username = set()

    def _gen_username(self):
        username = self.fake.user_name()
        if username in self._username:
            self._gen_username()
        else:
            self._username.add(username)
        return username

    def __init__(
            self,
            number_of_users=None,
            max_posts_per_user=None,
            max_likes_per_user=None,
            api_sleep=None,
            user_avatar=None,
            # Defaults of start_date and end_date are setting up in generate_post method
            start_date=None,
            end_date=None,
            max_post_length=None,
            image_generation=None,
            images_chance=None,
            unsplash_key=None,
    ):
        self.data = get_yaml('generator')
        self.fake = Faker()
        self.NUMBER_OF_USERS = number_of_users or hard_get(self.data, 'number_of_users')
        self.MAX_POSTS_PER_USER = max_posts_per_user or hard_get(self.data, 'max_posts_per_user')
        self.MAX_LIKES_PER_USER = max_likes_per_user or hard_get(self.data, 'max_likes_per_user')

        self.API_SLEEP = api_sleep or soft_get(self.data, 'api_sleep', float)

        self.START_DATETIME = start_date or soft_get(self.data, 'start_date', dt.date)
        self.END_DATETIME = end_date or soft_get(self.data, 'end_date', dt.date)

        self.MAX_POST_LENGTH = max_post_length or soft_get(self.data, 'max_post_length', int)

        self.IMAGE_GENERATION = image_generation or soft_get(self.data, 'image_generation', bool)
        if self.IMAGE_GENERATION:
            self.IMAGES_CHANCE = images_chance or soft_get(self.data, 'images_chance', float)
            self.UNSPLASH_KEY = unsplash_key or hard_get(self.data, 'unsplash_key')

    @staticmethod
    def generate_like(user):
        post = choice(Post.objects.all())
        like = Like.objects.get(post=post)
        like.user.add(user)

    def generate_post(self, user):

        date = self.fake.date_time_between(
            start_date=user.date_joined,
            end_date=self.END_DATETIME,
            tzinfo=timezone('Europe/Kiev'),
        )
        title = ' '.join(self.fake.words(
            nb=randint(1, 5),
            ext_word_list=None,
            unique=False
        )
        ).upper()

        text = self.fake.text(max_nb_chars=randint(100, self.MAX_POST_LENGTH), ext_word_list=None)

        post = Post(title=title,
                 text=text,
                 creator=user)
        post.save()

        if self.IMAGE_GENERATION:
            chance = randint(1, 100)
            if chance <= self.IMAGES_CHANCE * 100:
                response = r.request('GET', rf'http://api.unsplash.com/photos/random/?client_id={self.UNSPLASH_KEY}')
                sleep(self.API_SLEEP)
                content = response.content
                content = content.decode("UTF-8")
                content = json.loads(content)
                url = content['urls']['regular']
                response = r.request('GET', url)
                sleep(self.API_SLEEP)
                image = os.path.join(MEDIA_ROOT, 'posts', f'{post.id}.png')
                with open(image, 'wb') as img:
                    img.write(response.content)
                post.image = image

        post.pub_date = date
        post.save()

        return post

    def generate_user(self):
        username = self._gen_username()
        email = self.fake.ascii_email()
        password = self.fake.ean(length=8)
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        date_joined = self.fake.date_time_between(
                start_date=self.START_DATETIME,
                end_date=self.END_DATETIME,
                tzinfo=timezone('Europe/Kiev'),
        )
        profile_info = dict(
            company=self.fake.company(),
            role=self.fake.job(),

            city=self.fake.city(),
            country=self.fake.country(),

            bio=self.fake.text(max_nb_chars=randint(50, 500)),
        )

        user = User(username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    date_joined=date_joined)
        user.set_password(password)
        user.save()

        profile = UserProfile.objects.get(owner=user)
        for key, val in profile_info.items():
            setattr(profile, key, val)
        profile.save()

        return user

    def generation(self):
        for _ in range(self.NUMBER_OF_USERS):
            u = self.generate_user()

            posts = randint(0, self.MAX_POSTS_PER_USER)

            for __ in range(posts):
                self.generate_post(u)

        users = User.objects.all()

        for user in users:
            likes = randint(0, self.MAX_LIKES_PER_USER)

            for _ in range(likes):
                self.generate_like(user)
