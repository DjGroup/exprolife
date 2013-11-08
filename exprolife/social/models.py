from django.db import models


class User(models.Model):
    firstName = models.CharField(max_length=30, blank=False, default=None)
    lastName = models.CharField(max_length=30, blank=False, default=None)
    email = models.EmailField(max_length=100, blank=False, default=None)
    password = models.CharField(max_length=100, blank=False, default=None)
    score = models.IntegerField(default=0)

    #male=0 female=1
    sex = models.BooleanField(blank=False, default=None)
    #image = models.ImageField()

    
class Competence(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=30, blank=False, default=None)
    description = models.TextField(max_length=100, blank=True, default=None)
    tags = models.CharField(max_length=50, blank=False, default=None)
    developers = models.CharField(max_length=50, blank=False, default=None)
    manager = models.CharField(max_length=20, blank=False, default=None)
    picture = models.ImageField(upload_to="uploads_image/", blank=True)
    releaseDate = models.DateField()
    sourceCode = models.FileField(upload_to="uploads_file/", blank=True)
    usage = models.CharField(max_length=50, blank=True, default=None)
    vote = models.IntegerField(default=0)


class BoardPost(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(max_length=1000, blank=False, default=None)
    #image = models.ImageField()
    tagList = models.CharField(max_length=1000, blank=False, default=None)
    vote = models.IntegerField(default=0)