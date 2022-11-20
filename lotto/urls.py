from django.urls import path
from django.contrib.auth import views

app_name = 'common'

urlpatterns = [
    path('', views.index),
    path('create_number/', views.create_num),
]