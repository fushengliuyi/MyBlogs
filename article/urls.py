from django.urls import path, re_path
from django.views.static import serve

from . import views
from Blogs.settings import MEDIA_ROOT

app_name = 'article'
urlpatterns = [
    path('index/', views.index, name='index'),  # 首页信息展示
    path('details/<int:article_id>/', views.blog_detail, name='details'),  # 详情信息展示
    path('login/', views.login, name='login'),  # 用户登录
    path('logout/', views.logout, name='logout'),  # 退出登录
    path('register/', views.register, name='register'),  # 用户注册
    path('is_login/', views.is_login, name='is_login'),  # 判断是否登录
    # path('cache_username/', views.cache_username, name='cache_username'),  # 用户名的 缓存获取

]
