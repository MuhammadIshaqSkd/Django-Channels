from django.shortcuts import render
from posts.models import Post
from posts.api.serializers import PostSerializer
from rest_framework import viewsets
from rest_framework.decorators import action


# Create your views here.


class PostViewSets(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(methods=['post'], detail=True)
    def like_post(self, request, pk):
        post = self.get_object()
