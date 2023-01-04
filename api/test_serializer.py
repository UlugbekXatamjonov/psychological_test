from rest_framework import serializers

from mytest.models import Category, Info, Form, Form_number, Test, Test_answer, Test_result


class Test_answerAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_answer
        fields = ('id','answer_text')


class TestAPISerializer(serializers.ModelSerializer):
    answer = Test_answerAPISerializer(many=True, read_only=True)
    class Meta:
        model = Test    
        fields = ('id','body','answer',)


class CategoryAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','slug','parent','body')
        

class SubCategoryAPISerializer(serializers.ModelSerializer):
    test_category = TestAPISerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('id','name','slug','parent','body','test_category')
        
""""""
""" Info modeli admin-api dan olinadi, alohida yozish shart emas """




