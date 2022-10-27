from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category


class PostList(ListView):
    ##post_list.html로 만들어야함
    model = Post # 기본설정post_list쪽으로 넘겨줌.
    # template_name = 'blog/index.html' #지정페이지사용법
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

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
    model = Post # 기본설정post_detail쪽으로 넘겨줌.
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