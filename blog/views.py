from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-pk')
    return render(
        request,
        'blog/index.html',
        {
            'adminPosts': posts,
        }
    )



# 기본 셋팅값
# def index(request):
#     return render(
#         request,
#     )