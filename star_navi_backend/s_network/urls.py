from django.urls import path
from .views import *

urlpatterns = [
    path('posts/all/', GetPosts.as_view()),
    path('posts/<str:username>/', GetPostsFiltered.as_view(), name='users_posts'),
    path('users/<id>/', GetUsers.as_view()),
    path('profile/<int:id>/', EditProfile.as_view()),
    path('like/<int:id>/', LikeDislike.as_view()),
]
