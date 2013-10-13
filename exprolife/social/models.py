from django.db import models


class User(models.Model):
    firstName = models.CharField(max_length=30, blank=False, default=None)
    lastName = models.CharField(max_length=30, blank=False, default=None)
    email = models.EmailField(max_length=100, blank=False, default=None)
    password = models.CharField(max_length=100, blank=False, default=None)
    score = models.IntegerField(default=0)

    #male=0 female=1
    sex = models.BooleanField()
    #image = models.ImageField()