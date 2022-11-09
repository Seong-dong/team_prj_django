from django.db import models
from django.contrib.auth.models import User
import os

from markdown import markdown
from markdownx.models import MarkdownxField
from datetime import timedelta

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True) #allow_unicode가 있어야 한글 입력 가능.
    #slug는 url텍스트 출력을 위해 설정.

    def __str__(self):
        return self.name

    def get_absolute_url(self): #get_absolute_url은 장고에서 젝오하는 기능.
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'


class Post(models.Model):
    title = models.CharField(max_length=50)
    hook_text = models.CharField(max_length=100, blank=True)
    #content = models.TextField()
    content = MarkdownxField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'
        #pk는 장고에서 제공하는 id값


    def get_absolute_url(self): #get_absolute_url은 장고에서 젝오하는 기능.
        return f'/blog/{self.pk}/'


    def get_file_name(self):
        return os.path.basename(self.file_upload.name)


    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    def get_content_markdown(self):
        return markdown(self.content)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): #admin페이지에서 보이는 상태
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def is_updated(self):
        return self.updated_at - self.created_at > timedelta(seconds=1)

    # def is_updated(self):
    #     return self.updated_at - self.created_at > timedelta(seconds=1)
    #
    # def get_avatar_url(self):
    #     if self.author.socialaccount_set.exists():
    #         return self.author.socialaccount_set.first().get_avatar_url()
    #     else:
    #         return f'https://doitdjango.com/avatar/id/143/e3445497d896a175/svg/{self.author.email}'