from django.shortcuts import render, get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Post, Contact
from .serializers import PostSerializer, ContactSerializer

# Create your views here.


class ContactViewset(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            new_contact = Contact.objects.create(
                full_name = data['full_name'],
                body = data['body'],
                age = data['age'],
                # read = data['read'],
            )
            new_contact.save()
            serializer = ContactSerializer(new_contact)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumot to'liq emas!!!"})

    def destroy(self, request, *args, **kvargs):
        contact = self.get_object()
        contact.status = 'delete'
        contact.delete()
        return Response({"message":"Ma'lumot muvaffaqiyatli o'chirildi."})


    def delete(self, request, *args, **kwargs):
        contact = self.get_object()
        if contact.status == 'delete':
            contact.delete()
        

    def update(self, request, *args, **kwargs):
        contact = self.get_object()
        data = request.data

        try:
            contact.full_name = data['full_name'] if 'full_name' in data else contact.full_name
            contact.body = data['body'] if 'body' in data else contact.body
            contact.age = data['age'] if 'age' in data else contact.age
            contact.read = data['read'] if 'read' in data else contact.read

            contact.save()
            serializer = ContactSerializer(contact)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            new_post = Post.objects.create(
                title = data['title'],
                body = data['body'],
                photo = data['photo'],
                # video = data['video'],
            )
            new_post.save()
            serializer = PostSerializer(new_post)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumot to'liq emas!!!"})

    def destroy(self, request, *args, **kvargs):
        post = self.get_object()
        post.status = 'delete'
        post.delete()
        return Response({"message":"Ma'lumot muvaffaqiyatli o'chirildi."})

    def delete(self, request, *args, **kwargs):
        contact = self.get_object()
        if contact.status == 'delete':
            contact.delete()
        return Response({"message":"Ma'lumot muvaffaqiyatli yo'q qilindi."})            

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        data = request.data

        try:
            post.title = data['title'] if 'title' in data else post.title
            post.body = data['body'] if 'body' in data else post.body
            post.photo = data['photo'] if 'photo' in data else post.photo
            # post.video = data['video'] if 'video' in data else post.video
            post.status = data['status'] if 'status' in data else post.status
            post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})




