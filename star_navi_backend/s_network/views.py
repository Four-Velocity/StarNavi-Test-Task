from .serializers import PostViewSerializer, UserViewSerializer, UserProfileSerializer
from rest_framework import generics, views
from .models import Post, User, UserProfile, Like
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from pyhunter import PyHunter
import clearbit


class GetPosts(generics.ListCreateAPIView):
    """
    List of all Posts with GET request
    Create new Post with POST request
    """
    queryset = Post.objects.all().order_by('-pub_date')
    serializer_class = PostViewSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(creator=user)


class ChangePosts(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update or delete single post
    """
    queryset = Post.objects.all()
    serializer_class = PostViewSerializer
    permission_classes = [IsOwnerOrReadOnly]

class GetPostsFiltered(generics.ListAPIView):
    """
    List of all Posts of current user
    """
    serializer_class = PostViewSerializer

    def get_queryset(self):
        """
        Filter posts by username, case match is not necessary (UserName == username == USERNAME)
        """
        username = self.kwargs['username']
        return Post.objects.filter(creator__username__iexact=username).order_by('-pub_date')


class GetUsers(generics.ListAPIView):
    """
    List of all users
    """
    permission_classes = [AllowAny]
    serializer_class = UserViewSerializer

    def get_queryset(self):
        """
        Show all users, or get one by id
        """
        id = self.kwargs['id']
        if id != 'all':
            return User.objects.get(pk=id),
        else:
            return User.objects.all()


class EditProfile(generics.UpdateAPIView):
    """
    Edit user profile
    """
    queryset = UserProfile.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        """
        Get profile by id
        """
        id = self.kwargs['id']
        return UserProfile.objects.get(pk=id),


class LikeDislike(generics.UpdateAPIView):
    """
    Like or dislike post
    """
    def put(self, request, *args, **kwargs):
        like = Like.objects.get(post=Post.objects.get(pk=self.kwargs['id']))
        user = request.user
        if user in like.user.all():
            like.user.remove(user)
            like.save()
            result = -1
        else:
            like.user.add(user)
            like.save()
            result = 1
        return Response({"result": result})

class Validation(views.APIView):
    """
    Validate email via pyhunter and get additional data from clearbit
    """
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        hunter = PyHunter(settings.EMAILHUNTER_KEY)
        clearbit.key = settings.CLEARBIT_KEY
        valid = hunter.email_verifier(email)
        content = dict(
            valid=valid['result'],
        )
        person = clearbit.Person.find(email=email, stream=True)
        if person is not None:
            content.update(dict(
                name=person['name']['fullName'],
                company=person['employment']['name'],
                role=person['employment']['role'],
                city=person['geo']['city'],
                country=person['geo']['country'],
                bio=person['bio'],
                avatar_url=person['avatar'],
            ))
        return Response(content)
