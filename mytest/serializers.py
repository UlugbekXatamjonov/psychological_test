from rest_framework import serializers

from .models import Category, Info, Form, Form_number, Test, Test_answer, Test_result


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')
        
class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ('__all__')

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ('__all__')

class Form_numberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form_number
        fields = ('__all__')

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('__all__')

class Test_answerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_answer
        fields = ('__all__')

class Test_resultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_result
        fields = ('__all__')




# class Serializers(serializers.ModelSerializer):
#     class Meta:
#         model = 
#         fields = ('__all__')

