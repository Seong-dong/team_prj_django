from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag


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

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category

        }
    )

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'tag': tag

        }
    )


# 기본 셋팅값
# def index(request):
#     return render(
#         request,
#     )