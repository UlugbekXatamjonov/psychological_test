from rest_framework import serializers

from mytest.models import Category, Info, Form, Form_number, Test, Test_answer, Test_result



class Test_answerAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_answer
        fields = ('id','test_id','answer_text')


class TestAPISerializer(serializers.ModelSerializer):
    answer = Test_answerAPISerializer(many=True, read_only=True)
    class Meta:
        model = Test    
        fields = ('id','body','category','answer',)


class CategoryAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','slug','parent','body')
        
        
""" Info modeli admin-api dan olinadi, alohida yozish shart emas """




