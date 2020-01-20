from django.urls import path
from . import views

app_name = 'article'
urlpatterns = [
    path('index/', views.index),  # 首页信息展示
    path('article/<int:article_id>/',views.article_detail), # 详情信息展示
]
