from rest_framework import serializers

from .models import Post, Contact


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')
                
        
class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('__all__')
             
