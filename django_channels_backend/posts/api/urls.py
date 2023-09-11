from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.api.views import PostViewSets

router = DefaultRouter()

router.register(r'post', PostViewSets, basename='post')

urlpatterns = [
    path('',include(router.urls))
]


