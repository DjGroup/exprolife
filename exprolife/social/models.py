from django.db import models


class User(models.Model):
    firstName = models.CharField(max_length=30, blank=False, default=None)
    lastName = models.CharField(max_length=30, blank=False, default=None)
    email = models.EmailField(max_length=100, blank=False, default=None)
    password = models.CharField(max_length=100, blank=False, default=None)
    score = models.IntegerField(default=0)

    #male=0 female=1
    sex = models.BooleanField(blank=False, default=None)
    # image = models.ImageField(upload_to="uploads_image/", default=None)

    studyField = models.CharField(max_length=500,blank=True)
    degrees = models.CharField(max_length=500, blank=True)
    honors = models.CharField(max_length=500, blank=True)
    languageSkills = models.CharField(max_length=500, blank=True)
    areasOfInterest = models.CharField(max_length=500, blank=True)
    nonAcademicInterest = models.CharField(max_length=500, blank=True)

    
class Competence(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100, blank=False, default=None)
    content = models.TextField(max_length=100, blank=True, default=None)
    tagList = models.CharField(max_length=100, blank=False, default=None)
    developers = models.CharField(max_length=200, blank=False, default=None)
    manager = models.CharField(max_length=100, blank=False, default=None)
    picture = models.FileField(upload_to="uploads_image/", blank=True)
    date = models.DateTimeField()
    sourceCode = models.FileField(upload_to="uploads_file/", blank=True)
    usage = models.CharField(max_length=1000, blank=True, default=None)
    vote = models.IntegerField(default=0)


class BoardPost(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(max_length=1000, blank=False, default=None)
    #image = models.ImageField()
    tagList = models.CharField(max_length=1000, blank=False, default=None)
    # vote = models.IntegerField(default=0)


class TraceShip(models.Model):
    userSender = models.ForeignKey(User, related_name="TraceShip_userSender")
    senderTime = models.DateTimeField()

    userReceiver = models.ForeignKey(User, related_name="TraceShip_userReceiver")
    receiverTime = models.DateTimeField()

    isUser2AcceptTrace = models.BooleanField(default=0, blank=None)
    isShowNotificationToUser2 = models.BooleanField(default=1, blank=None)
    isShowNotificationToUser1 = models.BooleanField(default=0, blank=None)


class CommentPost(models.Model):
    user = models.BigIntegerField(blank=False)
    content = models.TextField(max_length=1000, blank=False, default=None)
    referencePost = models.ForeignKey(BoardPost, blank=False)
    referenceComment = models.BigIntegerField(blank=False, default=0)
    depth = models.PositiveSmallIntegerField(blank=False, default=0)
    user_notification = models.BooleanField(default=1, blank=None)
    main_notification = models.BooleanField(default=0, blank=None)
    time = models.DateTimeField()


class CommentCompetence(models.Model):
    user = models.BigIntegerField(blank=False)
    content = models.TextField(max_length=1000, blank=False, default=None)
    referenceCompetence = models.ForeignKey(Competence, blank=False)
    referenceComment = models.BigIntegerField(blank=False, default=0)
    depth = models.PositiveSmallIntegerField(blank=False, default=0)
    user_notification = models.BooleanField(default=1, blank=None)
    main_notification = models.BooleanField(default=0, blank=None)
    time = models.DateTimeField()


class userProjectRate(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Competence)
    rate = models.IntegerField(default=0)