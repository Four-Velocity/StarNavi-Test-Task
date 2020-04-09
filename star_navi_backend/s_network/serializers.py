from rest_framework import serializers
from .models import User, UserProfile, Post, Like


class LikePkListField(serializers.RelatedField):
    def to_representation(self, value):
        return [user.id for user in value.user.all()]


class UserShortField(serializers.RelatedField):
    def to_representation(self, value):
        return dict(
            id=value.id,
            username=value.username,
            avatar=value.profile.avatar.url,
        )


class PostViewSerializer(serializers.ModelSerializer):
    likes_list = LikePkListField(read_only=True)
    creator = UserShortField(read_only=True)
    text = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = (
            'id',
            'title', 'image', 'text',
            'likes', 'pub_date',
            'creator', 'likes_list',)



class UserProfileField(serializers.RelatedField):
    def to_representation(self, value):
        return dict(
            id=value.id,
            username=value.owner.username,
            email=value.owner.email,
            full_name=f'{value.owner.first_name} {value.owner.last_name}',
            company=value.company,
            role=value.role,
            city=value.city,
            country=value.country,
            bio=value.bio,
            avatar=value.avatar.url,
        )


class UserViewSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedIdentityField(view_name='users_posts', lookup_field='username')
    profile = UserProfileField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'is_active',
                  'profile', 'posts',)
        read_only_fields = ('id', 'is_active')


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = UserProfile
        fields = ('company', 'role',
                  'city', 'country',
                  'bio',
                  'avatar',)
