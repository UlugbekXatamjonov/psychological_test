from rest_framework import serializers

from mytest.models import Category, Info, Form, Test, Test_answer


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
        

class InfoAPISerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    class Meta:
        model = Info
        fields = ("id",'category_name','full_name','age', 'gender', 'test_ball', "test_result")




