from rest_framework import serializers

from .models import Category, Info, Form, Form_number, Test, Test_answer, Test_result


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class InfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ('__all__')

class FormSerializers(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ('__all__')

class Form_numberSerializers(serializers.ModelSerializer):
    class Meta:
        model = Form_number
        fields = ('__all__')

class TestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('__all__')

class Test_answerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Test_answer
        fields = ('__all__')

class Test_resultSerializers(serializers.ModelSerializer):
    class Meta:
        model = Test_result
        fields = ('__all__')




# class Serializers(serializers.ModelSerializer):
#     class Meta:
#         model = 
#         fields = ('__all__')

