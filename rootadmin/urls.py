from django.urls import path

from rootadmin import views

app_name = 'rootadmin'

urlpatterns = [
    path('index/', views.index),  # 后台管理页面首页
]
