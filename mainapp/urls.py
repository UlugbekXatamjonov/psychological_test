from django.urls import path, include
from rest_framework import routers

from .views import ContactViewset, PostViewset, Personal_InfoViewset


router = routers.DefaultRouter()
router.register(r'post', PostViewset, basename='post')
router.register(r'contact', ContactViewset, basename='contact')
router.register(r'personal_info', Personal_InfoViewset, basename='personal_info')

urlpatterns = [
	path('', include(router.urls)),
]

