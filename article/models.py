from django.db import models


# Create your models here.

# 文章
class Article(models.Model):
    title = models.CharField(max_length=128)  # 标题
    content = models.TextField()

    class Meta:
        db_table = "article"


