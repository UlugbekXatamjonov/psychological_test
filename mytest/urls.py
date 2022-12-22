from django.urls import path, include
from rest_framework import routers

from .views import CategoryViewSet, InfoViewSet, FormViewSet, Form_numberViewSet, TestViewSet, TestAnswerViewSet, TestResultViewSet


router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'info', InfoViewSet, basename="info")
router.register(r'form', FormViewSet, basename="form")
router.register(r'form-number', Form_numberViewSet, basename="form-number")
router.register(r'test', TestViewSet, basename="test")
router.register(r'answer', TestAnswerViewSet, basename="answer")
router.register(r'result', TestResultViewSet, basename="result")

urlpatterns = [	
	path('', include(router.urls)),
]

