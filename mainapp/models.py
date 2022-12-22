from django.db import models

from autoslug import AutoSlugField

# Create your models here.


STATUS = (
    ('active','Active'),
    ('deactive','Deactive'),
    ('delete','Delete')
)

class Contact(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="Ism sharif")
    slug = AutoSlugField(populate_from='full_name', unique=True)
    age = models.PositiveIntegerField(verbose_name="Yosh")
    body = models.TextField(verbose_name="Matn")
    read = models.BooleanField(default=False, verbose_name="O'qildi")
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering   = ("-read", "-created_at")

    def __str__(self):
        return self.full_name
    
    
    
class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name="Sarlavha")
    slug = AutoSlugField(populate_from='title', unique=True,)
    body = models.TextField(verbose_name="Matn")
    photo = models.ImageField(upload_to='photos/', verbose_name="Rasm", blank=True, null=True)
    video = models.FileField(upload_to='videos/', verbose_name="Video", blank=True, null=True)
    status = models.CharField(max_length=25, choices=STATUS, default='active', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering  = ("-created_at",)

    def __str__(self):
        return self.title





