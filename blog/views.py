from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-pk')
    return render(
        request,
        'blog/index.html',
        {
            'contentsPost': posts, # ./blog/index.html로 adminPosts변수로 보낼수있음.
        }
    )

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/single_page.html',
        {
            'post': post,
        }
    )


# 기본 셋팅값
# def index(request):
#     return render(
#         request,
#     )