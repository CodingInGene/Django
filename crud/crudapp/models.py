from django.db import models
from django.shortcuts import reverse

# Create your models here.
class Entries(models.Model):
    name = models.CharField(max_length=30)
    phone = models.IntegerField()
    email = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    pin = models.IntegerField()
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.datetime)