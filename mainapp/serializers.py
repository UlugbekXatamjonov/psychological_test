from rest_framework import serializers

from .models import Post, Contact


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
                
        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('__all__')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
             
