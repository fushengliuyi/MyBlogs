from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail
from django.contrib.contenttypes.fields import GenericRelation


# 文章类型
class BlogType(models.Model):
    type_name = models.CharField(max_length=32)
    type_images = models.ImageField(upload_to='article/blog_images/')

    class Meta:
        db_table = 'blog_type'

    def __str__(self):
        return f'{self.type_name}'


# 用户
class User(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField()
    password = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.username}'


# 文章
class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=128)  # 标题
    content = RichTextUploadingField()
    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    read_details = GenericRelation(ReadDetail)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "article"
        ordering = ['id', ]

    def __str__(self):
        return f'{self.title}'
