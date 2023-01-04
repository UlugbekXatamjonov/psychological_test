from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response 
from rest_framework import viewsets

from mytest.models import Category, Info, Form, Form_number, Test, Test_answer, Test_result
from .test_serializer import TestAPISerializer, CategoryAPISerializer, SubCategoryAPISerializer
    
class CategoryAPIViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
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
    queryset = Category.objects.all()
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
    queryset = Test.objects.all()
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
    
    # def update(self, request, *args, **kwargs):
    #     test_data = self.get_object()
    #     data = request.data

    #     # <--- Category uchun --->
    #     try:
    #     	try:
    #        		category = Category.objects.filter(pk=data['category']).first()
    #     	except:
    #         		category = None
    #     except Exception as e:
    #         return Response({"error":"Bunday  Kata kategoriya mavjud emas!!!"})
        
    #     # <--- Form_number uchun   --->
    #     try:
    #     	try:
    #        		form = Form.objects.filter(pk=data['form']).first()
    #     	except:
    #         		form = None
    #     except Exception as e:
    #         return Response({"error":"Bunday  Forma mavjud emas!!!"})
    #     # <--- Foreginkey uchun --->
        
    #     try:
    #         if category:
    #             test_data.form = form
    #             test_data.category = category
    #             test_data.body = data['body'] if 'body' in data else test_data.body
    #         else:
    #             test_data.form = form
    #             test_data.body = data['body'] if 'body' in data else test_data.body
    #         test_data.save()
    #         serializer = TestAPISerializer(test_data)
    #         return Response(serializer.data)
    #     except Exception as e:
    #         return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})


