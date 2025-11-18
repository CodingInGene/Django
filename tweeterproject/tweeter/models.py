from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.TextField(max_length=240)
    image = models.ImageField(upload_to="photos/")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username+" "+str(self.created_at)