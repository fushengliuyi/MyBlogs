from django.db import models
from django.contrib.auth.models import User


# 文章类型
class BlogType(models.Model):
    type_name = models.CharField(max_length=32)
    type_images = models.ImageField(upload_to='article/blog_images/')

    class Meta:
        db_table = 'blog_type'

    def __str__(self):
        return f'{self.type_name}'


# 文章
class Blog(models.Model):
    title = models.CharField(max_length=128)  # 标题
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "article"

    def __str__(self):
        return f'{self.title}'
