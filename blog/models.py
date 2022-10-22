from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'[{self.pk}] {self.title}' #pk는 장고에서 제공하는 id값

    def get_absolute_url(self): #get_absolute_url은 장고에서 젝오하는 기능.
        return f'/blog/{self.pk}/'