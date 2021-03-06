import datetime
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from article import models, forms
import hashlib

from article.models import Blog
from read_statistics.utils import read_statistics_once_read, get_today_hot_data, get_yesterday_hot_data, get_7_hot_data
from django.contrib.contenttypes.models import ContentType

from django.core.cache import cache
from comment.models import Comment
import time


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

# 周热搜查询
def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date) \
        .values('id', 'title', 'created_time', 'content') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[:6]


# 博客首页
def index(request):
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

    # 热搜数据的查询
    blog_content_type = ContentType.objects.get_for_model(models.Blog)

    # # 昨日热搜
    # yesterday_hot_data = get_yesterday_hot_data(blog_content_type)

    # 今日热搜
    # today_hot_data = get_today_hot_data(blog_content_type)

    # 获取 7天热门 博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')

    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 60 * 60)
    # # 周热搜
    hot_data_for_7_days = hot_blogs_for_7_days
    times = time.strftime('%m-%d')

    return render(request, 'article/index.html', locals())


# 博客详情
def blog_detail(request, article_id):
    content = get_object_or_404(models.Blog, id=int(article_id))
    read_cookie_key = read_statistics_once_read(request, content)

    # 热搜数据的查询
    blog_content_type = ContentType.objects.get_for_model(models.Blog)

    # 今日热搜数据
    today_hot_data = get_today_hot_data(blog_content_type)

    # 相关评论类容
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=content.pk, parent=None)

    response = render(request, 'article/article.html', locals())
    response.set_cookie(read_cookie_key, 'true')
    return response


# 用户注册
def register(request):
    errmsg = {'errmsg': ''}
    if request.method == 'POST':
        # 创建表单实例
        userform = forms.UserForms(request.POST)
        print(request.POST)
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

        # 记录上一次的页面
        last_url = request.META.get('HTTP_REFERER')
        response = redirect(last_url)

        # 判断用户
        user = models.User.objects.filter(email=email).first()
        if user:
            user.password = set_password(password)
            # 设置 cookie和session
            response.set_cookie('email', email)
            response.set_cookie('username', user.username)
            request.session['email'] = email

            # 设置缓存
            cache.set('username', user.username)
        return response


# 判断 用户是否登录
def is_login(request):
    result = {'code': 400}
    if request.method == 'POST':
        cookie_email = request.COOKIES.get('email')
        session_email = request.session.get('email')

        if cookie_email and session_email and cookie_email == session_email:
            result['code'] = 200

    return JsonResponse(result)


# # 用户名缓存获取
# def cache_username(request):
#     result = {'code': 200}
#     result['username'] = cache.get('username')
#     return JsonResponse(result)


def logout(request):
    last_url = request.META.get('HTTP_REFERER')
    response = redirect(last_url)
    response.delete_cookie('email')
    response.delete_cookie('username')
    request.session.flush()
    return response
