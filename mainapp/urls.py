from django.urls import path, include
from rest_framework import routers

from .views import ContactViewset, PostViewset


router = routers.DefaultRouter()
router.register(r'post', PostViewset, basename='post')
router.register(r'contact', ContactViewset, basename='contact')

urlpatterns = [
	path('', include(router.urls)),
]

