from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView

from .forms import BoardForm
from .models import Board
# Create your views here.



class BoardList(ListView):
    ##board_list.html로 만들어야함
    model = Board
    # template_name = 'blog/index.html' #지정페이지사용법
    ordering = '-pk'
    paginate_by = 10
    #
    # def get_context_data(self, **kwargs):
    #     context = super(PostList, self).get_context_data()
    #     context['categories'] = Category.objects.all()
    #     context['no_category_post_count'] = Post.objects.filter(category=None).count()
    #     return context

class BoardDetail(DetailView):
    model = Board

class BoardCreate(LoginRequiredMixin, CreateView):
    model = Board
    form_class = BoardForm
    #
    # def test_func(self):
    #     return self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_active #유저 권한 체크


    def form_valid(self, form): #form 은 현재 class의 instance
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            response = super(BoardCreate, self).form_valid(form)

            return response
        else:
            return redirect('/board/')