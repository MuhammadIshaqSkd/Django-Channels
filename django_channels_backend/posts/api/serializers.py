from rest_framework import serializers
from posts.models import Post
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class PostSerializer(serializers.ModelSerializer):
    likes = UserSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_author(self, obj):
        return obj.author.username

    def get_like_count(self,obj):
        return len(obj.likes.all())
