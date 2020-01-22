from django.urls import path
from . import views

app_name = 'article'
urlpatterns = [
    path('index/', views.index),  # 首页信息展示
    path('details/<int:article_id>/', views.blog_detail),  # 详情信息展示
]
