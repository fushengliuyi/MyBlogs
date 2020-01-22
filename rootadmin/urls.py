from django.urls import path

from rootadmin import views

app_name = 'rootadmin'

urlpatterns = [
    path('index/', views.index, name='index'),  # 后台管理页面首页
    path('login/', views.login, name='login'),  # 登录页面展示
    path('register/', views.register, name='register'),  # 注册页面展示
]
