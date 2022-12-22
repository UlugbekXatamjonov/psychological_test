from django.urls import path, include
from rest_framework import routers

from .views import PostViewSet
from .test_view import TestAPIViewSet, CategoryAPIViewSet

router = routers.DefaultRouter()
router.register(r'post', PostViewSet, basename='post')
router.register(r'test', TestAPIViewSet, basename='test')
router.register(r'category', CategoryAPIViewSet, basename='category')

urlpatterns = [
	path('', include(router.urls)),
]

