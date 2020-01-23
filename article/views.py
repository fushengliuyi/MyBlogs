from django.shortcuts import render, get_object_or_404
from . import models


# Create your views here.

def index(request):
    blog_type = request.GET.get('blog_type')
    if blog_type:
        blog_type_all = models.Blog.objects.filter(blog_type=blog_type)
        return render(request, 'article/index.html', locals())
    article = models.Blog.objects.all()
    blog_type = models.BlogType.objects.all()
    return render(request, 'article/index.html', locals())


# 博客详情
def blog_detail(request, article_id):
    content = get_object_or_404(models.Blog, id=int(article_id))
    return render(request, 'article/article.html', locals())
