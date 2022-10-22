from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    ##post_list.html로 만들어야함
    model = Post
    # template_name = 'blog/index.html' #지정페이지사용법
    ordering = '-pk'

# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'contentsPost': posts, # ./blog/index.html로 adminPosts변수로 보낼수있음.
#         }
#     )


class PostDetail(DetailView):
    ##post_list.html로 만들어야함
    model = Post
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/single_page.html',
#         {
#             'post': post,
#         }
#     )


# 기본 셋팅값
# def index(request):
#     return render(
#         request,
#     )