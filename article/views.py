from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from article import models, forms
import hashlib

from read_statistics.utils import read_statistics_once_read


# md5密码加密
def set_password(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    result = md5.hexdigest()
    return result


# 用户名  头像   装饰器
# def outer(func):
#     def inner(request, *args, **kwargs):
#         # 获取cookie
#         cookie_email = request.COOKIES.get('email')
#         session_email = request.session.get('email')
#
#         user = models.User.objects.filter(email=cookie_email).first()
#
#         if cookie_email and session_email and cookie_email == session_email:
#             kwargs['user'] = user
#             users = func(request, *args, **kwargs)
#             return users
#         else:
#             response = HttpResponseRedirect(reverse('article:index'))
#             return response


# 博客首页
def index(request, **kwargs):
    blog_type = request.GET.get('blog_type')
    page = request.GET.get('page')

    if page:
        page = int(page)
    else:
        page = 1

    blog_type_all = models.Blog.objects.all()

    if blog_type:
        blog_type_all = models.Blog.objects.filter(blog_type=blog_type)

    paginator = Paginator(blog_type_all, 20)
    article = paginator.page(page)

    blog_type = models.BlogType.objects.all()
    return render(request, 'article/index.html', locals())


# 博客详情
def blog_detail(request, article_id):
    content = get_object_or_404(models.Blog, id=int(article_id))
    read_cookie_key = read_statistics_once_read(request, content)

    response = render(request, 'article/article.html', locals())
    response.set_cookie(read_cookie_key, 'true')
    return response


# 用户注册
def register(request):
    errmsg = {'errmsg': ''}
    if request.method == 'POST':
        # 创建表单实例
        userform = forms.UserForms(request.POST)
        # 发起校验
        if userform.is_valid():
            # 获取数据
            data = userform.cleaned_data

            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # 获取用户对象
            user = models.User()
            user.username = username
            user.email = email
            user.password = set_password(password)

            user.save()
        else:
            errmsg['errmsg'] = '你提交的数据有误！'
        return render(request, 'article/index.html', locals())


# 用户登录
def login(request):
    if request.method == 'POST':
        errmsg = {'errmsg': ''}
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = models.User.objects.filter(email=email).first()
        if user:
            user.password = set_password(password)

        return render(request, 'article/index.html', locals())
