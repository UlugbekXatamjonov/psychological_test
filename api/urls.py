from django.urls import path, include
from rest_framework import routers

from .views import PostViewSet, Personal_InfoAPIViewSet
from .test_views import TestAPIViewSet, CategoryAPIViewSet, SubCategoryAPIViewSet, InfoAPIViewSet


router = routers.DefaultRouter()
router.register(r'post', PostViewSet, basename='post')
router.register(r'personal_info', Personal_InfoAPIViewSet, basename='personal_info')

router.register(r'test', TestAPIViewSet, basename='test')
router.register(r'category', CategoryAPIViewSet, basename='category')
router.register(r'subcategory', SubCategoryAPIViewSet, basename='subcategory')
router.register(r'info', InfoAPIViewSet, basename='info')


urlpatterns = [	
	path('', include(router.urls)),
]




