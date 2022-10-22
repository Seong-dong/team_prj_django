from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.single_post_page), #views.py의 single_post_page 함수
    # path('', views.index), #views.py의 index함수 ##FBV
    path('', views.PostList.as_view()),
]