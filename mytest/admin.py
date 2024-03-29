from django.contrib import admin

from .models import Category, Info, Form, Test, Test_answer

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name','id','slug','parent','category_form','status','created_at')
	list_filter = ('status','created_at')
	search_field = ('name','category_form','body')

@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
	list_display = ('full_name','category','id','slug','age','gender','status','created_at')
	list_filter = ('gender','status','category','created_at')
	search_field = ('full_name','category','age')

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
	list_display = ('name','id','slug','status','created_at')
	list_filter = ('status','created_at')

# Test_answer uchun Inline panel
class TestAnswerInlineMode(admin.TabularInline):
    model = Test_answer
    fields = ['test_id','answer_text','ball','status',]

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
	list_display = ('category','id','form','status','created_at')
	list_filter = ('category','form','status','created_at')
	search_field = ('body',)
	inlines = [TestAnswerInlineMode,]


@admin.register(Test_answer)
class Test_answerAdmin(admin.ModelAdmin):
	list_display = ('answer_text','test_id','ball','status','created_at')
	list_filter = ('ball','status','created_at')
	search_field = ('answer_text',)


# @admin.register()
# class Admin(admin.ModelAdmin):
# 	list_display = ('','','','','','','')
# 	list_filter = ('','','','','','','')
# 	search_field = ('','','','','','','')
