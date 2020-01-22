from django.contrib import admin
from .models import Blog, BlogType


# Register your models here.
# admin.site.register(Article)

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog_type', 'content', 'author', 'created_time', 'last_update_time')
    ordering = ('-id',)
