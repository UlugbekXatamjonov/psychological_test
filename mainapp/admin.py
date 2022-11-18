from django.contrib import admin


from .models import Contact, Post

# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'age', 'read', 'created_at')
	list_filter = ('read', 'created_at')
	ordered_by  =('-read', '-created_at')


@admin.register(Post)
class BlogAdmin(admin.ModelAdmin):
	list_display = ('title', 'status', 'created_at')
	list_filter = ('status', 'created_at')
	ordered_by  =('-status', '-created_at')


