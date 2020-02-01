from django.shortcuts import render, redirect
from . import models
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from article.models import User
import time
from .forms import CommentForm


# Create your views here.


def submit_comment(request):
    result = {'code': 400}
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()

        comment_text = request.POST.get('comment').strip()
        obj_id = int(request.POST.get('object_id'))
        content_type = request.POST.get('content_type')

        parrent_username = request.POST.get('parrent_username')

        reply_id = request.POST.get('reply_comment_id')
        parent_id = models.Comment.objects.filter(id=reply_id).first()

        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=obj_id)

        comment = models.Comment()
        comment.user = user
        comment.text = comment_text
        comment.content_object = model_obj
        comment.comment_time = time.time()
        if parent_id:
            comment.root = parent_id
            comment.parent = parent_id
            username = User.objects.filter(username=parrent_username).first()
            comment.reply_to = username
        comment.save()

        result['code'] = 200
        result['username'] = comment.user.username
        result['comment_time'] = comment.comment_time.strftime('%Y-%m-%d')
        result['text'] = comment.text
    return JsonResponse(result)
