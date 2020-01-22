from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=32)  # 用户名
    email = models.EmailField(unique=True)  # 邮箱
    password = models.CharField(max_length=32)  # 密码
    pricture = models.ImageField(upload_to='img', default=r'\static\rootadmin\img\default.jpg')

    class meta:
        db_table = 'AdminUser'
