from django.db import models
import os

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'[{self.pk}] {self.title}' #pk는 장고에서 제공하는 id값


    def get_absolute_url(self): #get_absolute_url은 장고에서 젝오하는 기능.
        return f'/blog/{self.pk}/'


    def get_file_name(self):
        return os.path.basename(self.file_upload.name)


    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]