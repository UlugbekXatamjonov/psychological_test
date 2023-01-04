from rest_framework import serializers

from mainapp.models import Post


class PostGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title','slug','body','photo')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }





