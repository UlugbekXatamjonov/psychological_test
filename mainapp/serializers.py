from rest_framework import serializers

from .models import Post, Contact


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
                
        
class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('__all__')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
             
