from django.urls import path, re_path
from django.views.static import serve

from . import views
from Blogs.settings import MEDIA_ROOT

app_name = 'article'
urlpatterns = [
    path('index/', views.index),  # 首页信息展示
    path('details/<int:article_id>/', views.blog_detail),  # 详情信息展示
]
