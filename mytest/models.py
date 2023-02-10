from django.db import models

from autoslug import AutoSlugField

# Create your models here.

STATUS = (
	('active','Active'),
	('deactive','Deactive'),
	('delete','Delete'),
)

GENDER = (
	('man','Erkak'),
	('woman','Ayol'),
)

DIAGNOSIS = (
	('bad','Sizning holatingiz yomon'),
	('normal','Sizning holatingiz yaxshi'),
	('well',"Sizning holatingiz a'lo"),
)


TUR = (
	('xavotir', "Xavotir HADS"),
 	('depressiya', "Depressiya HADS"),
	('boshqa', "Boshqa"),
	('yoq', "Yo'q")
)

class Category(models.Model):
	name = models.CharField(max_length=250, unique=True, verbose_name="Categoriya nomi")
	slug = AutoSlugField(populate_from='name', unique=True)
	# <<<---------- o'zini o'ziga ForeginKey orqali bog'lash ----------------->>> 
	parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Yuqori kategoriya")
	# <<<---------- o'zini o'ziga ForeginKey orqali bog'lash ----------------->>> 
	body = models.TextField(verbose_name="Kategoriya haqida", blank=True, null=True)
	category_form = models.BooleanField(default=False, verbose_name="Kategoriyada formula bor/yo'q", blank=True, null=True)
	ball35 = models.PositiveIntegerField(verbose_name="Formulaga qo'shiladigan ball", default=0,  blank=True, null=True)
	tur = models.CharField(max_length=50, choices=TUR, default='yoq' ,null=True, blank=True)	
 
	status = models.CharField(max_length=50, choices=STATUS, default='active', verbose_name="Holati")
	
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ("-created_at",)

	def __str__(self):
		return self.name

	def total_test_number():
		pass


class Info(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="info_category", verbose_name="Kategoriya")
	full_name = models.CharField(max_length=200, verbose_name="Ism Familya")
	slug = AutoSlugField(populate_from='full_name', unique=True)
	age = models.PositiveIntegerField(verbose_name="Yoshi")
	gender = models.CharField(max_length=50, choices=GENDER, default='man', verbose_name="Jinsi")
	test_ball = models.PositiveIntegerField(default=1, verbose_name="Testning yakuniy balli", null=True, blank=True)	
	test_result = models.CharField(max_length=25, verbose_name="Tashxis", null=True, blank=True)
	test_api = models.JSONField(default={}, null=True, blank=True)
 
	status = models.CharField(max_length=50, choices=STATUS, default='active', verbose_name="Holati")

	created_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ("-created_at",)

	def __str__(self):
		return self.full_name

	def total_score():
		pass


class Form(models.Model):
	name = models.CharField(max_length=50, unique=True,  verbose_name="Formula nomi: E1/E2...")
	slug = AutoSlugField(populate_from='name', unique=True)
	
	status = models.CharField(max_length=50, choices=STATUS, default='active', verbose_name="Holati")

	created_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ("-created_at",)

	def __str__(self):
		return self.name



class Test(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="test_category", verbose_name="Kategoriya")
	form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="test_form", blank=True, null=True ,verbose_name="Form")
	body = models.TextField(verbose_name="Test matni")
	slug = AutoSlugField(populate_from="category", unique=True)

	status = models.CharField(max_length=50, choices=STATUS, default='active', verbose_name="Holati")

	created_at  =models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ("-created_at",)

	def __str__(self):
		return self.body


class Test_answer(models.Model):
	test_id = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="answer", verbose_name="Test")	
	answer_text = models.TextField(verbose_name="Test varianti")
	ball = models.PositiveIntegerField(verbose_name="Variant ostidagi ball")
	status = models.CharField(max_length=50, choices=STATUS, default='active', verbose_name="Holati")

	created_at  =models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ("-created_at",)

	def __str__(self):
		return self.answer_text


