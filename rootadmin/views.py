from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import hashlib

# Create your views here.

# MD5 加密
from rootadmin import forms, models


def set_password(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    result = md5.hexdigest()
    return result


def outer(func):
    def inner(request, *args, **kwargs):
        # 获取 cookie
        cookie_email = request.COOKIES.get('email')
        session_email = request.session.get('email')

        user = models.User.objects.filter(email=cookie_email).first()

        if cookie_email and session_email and cookie_email == session_email:
            kwargs['user'] = user
            users = func(request, *args, **kwargs)
            return users
        else:
            response = HttpResponseRedirect('/rootadmin/login/')
            return response

    return inner


# 首页展示
def index(request):
    return render(request, 'rootadmin/index.html')


# login页面展示
def login(request):
    if request.method == 'POST':
        errmsg = {'errmsg': ''}
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')

        user = models.User.objects.filter(email=email).first()
        if user:
            if user.password == set_password(pwd):
                response = HttpResponseRedirect('/rootadmin/index/')

                # 设置 cookie email
                response.set_cookie('email', email)

                # 设置session email
                request.session['email'] = email

                return response
            else:
                errmsg['errmsg'] = '密码不正确！'

        else:
            errmsg['errmsg'] = '用户不存在！'

    return render(request, 'rootadmin/login.html', locals())


# register 页面注册
def register(request):
    errmsg = ''
    if request.method == 'POST':
        # 创建表单实例
        userform = forms.UserForms(request.POST)
        # 校验
        if userform.is_valid():
            # 获取数据
            data = userform.cleaned_data
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # 存储进数据库
            user = models.User()
            user.username = username
            user.password = set_password(password)
            user.email = email
            user.save()
            return redirect('rootadmin:login')
        errmsg = '您提交的数据有误！'

    return render(request, 'rootadmin/register.html', locals())
