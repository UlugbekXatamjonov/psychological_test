from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
# from rest_framework.decorators import 
from rest_framework import viewsets

from mainapp.models import Post
from mainapp.serializers import PostSerializers

from .serializers import PostSerializer


# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.filter(status="active")
	serializer_class = PostSerializer
	pagination_class = None
	permission_classes = [AllowAny]
	lookup_field = 'slug'

	def create(self, request, *args, **kwargs):
		return Response({"success":"Ma'lumotlar muvaffaqiyatli qo'shildi. -:)"})
	
	def destroy(self, request, *args, **kwargs):
		return Response({"success":"Ma'lumotlar muvaffaqiyatli o'chirildi. -:)"})
	
	def partial_update(self, request, *args, **kwargs):
		return Response({"success":"Ma'lumotlar muvaffaqiyatli yangilandi. -:)"})

	def update(self, request, *args, **kwargs):
		return Response({"success":"Ma'lumotlar muvaffaqiyatli yangilandi. -:)"})


