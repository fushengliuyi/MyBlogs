from django.shortcuts import render
from .models import Article


# Create your views here.

def index(request):
    article = Article.objects.all()
    return render(request, 'article/index.html', locals())


# 文章详情
def article_detail(request, article_id):
    return render(request, 'article/article.html')
