from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response 
from rest_framework import viewsets

from mytest.models import Category, Info, Form, Form_number, Test, Test_answer, Test_result
from .test_serializer import TestAPISerializer, CategoryAPISerializer, SubCategoryAPISerializer
    
class CategoryAPIViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(status="active")
    serializer_class = CategoryAPISerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
    		return Response({"success":"Ma'lumotlar muvaffaqiyatli qo'shildi. -:)"})
	
    def destroy(self, request, *args, **kwargs):
        return Response({"success":"Ma'lumotlar muvaffaqiyatli o'chirildi. -:)"})
	
    def partial_update(self, request, *args, **kwargs):
        return Response({"success":"Ma'lumotlar muvaffaqiyatli yangilandi. -:)"})
    
    def update(self, request, *args, **kwargs):
        return Response({"success":"Ma'lumotlar muvaffaqiyatli yangilandi. -:)"})


class SubCategoryAPIViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(status="active")
    serializer_class = SubCategoryAPISerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
    		return Response({"success":"Ma'lumotlar muvaffaqiyatli qo'shildi. -:)"})
	
    def destroy(self, request, *args, **kwargs):
        return Response({"success":"Ma'lumotlar muvaffaqiyatli o'chirildi. -:)"})
	
    def partial_update(self, request, *args, **kwargs):
        return Response({"success":"Ma'lumotlar muvaffaqiyatli yangilandi. -:)"})
    
    def update(self, request, *args, **kwargs):
        return Response({"success":"Ma'lumotlar muvaffaqiyatli yangilandi. -:)"})


class TestAPIViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.filter(status="active")
    serializer_class = TestAPISerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
    		return Response({"success":"Ma'lumotlar muvaffaqiyatli qo'shildi. -:)"})
	
    def destroy(self, request, *args, **kwargs):
        return Response({"success":"Ma'lumotlar muvaffaqiyatli o'chirildi. -:)"})
	
    def partial_update(self, request, *args, **kwargs):
        return Response({"success":"Ma'lumotlar muvaffaqiyatli yangilandi. -:)"})

    def update(self, request, *args, **kwargs):
        return Response({"success":"Ma'lumotlar muvaffaqiyatli yangilandi. -:)"})
    
   