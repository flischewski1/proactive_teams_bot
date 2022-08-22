from django.db import models

# Create your models here.


class Team(models.Model):
    id = models.AutoField(auto_created = True, primary_key = True, serialize = False, verbose_name ='ID' )  
    teamid = models.CharField(max_length=200,unique=True)
    displayName = models.CharField(max_length=200)
    relevant = models.BooleanField()

    def __str__(self):
        return self.teamid

class User(models.Model):
    id = models.AutoField(auto_created = True, primary_key = True, serialize = False, verbose_name ='ID' )  
    userid = models.CharField(max_length=200, unique=True)
    displayName = models.CharField(max_length=200)
    firstmessage = models.DateTimeField(null=True, blank=True)
    firstlogindate = models.DateTimeField(null=True, blank=True)
    teamid = models.ManyToManyField(Team)

    def __str__(self):
        return self.displayName


class Channel(models.Model): 
    id = models.AutoField(auto_created = True, primary_key = True, serialize = False, verbose_name ='ID' )  
    teamid = models.ForeignKey(Team, on_delete = models.CASCADE)
    channelid = models.CharField(max_length=200, unique=True)
    displayName = models.CharField(max_length=200)

    def __str__(self):
        return self.displayName


class Messages(models.Model):
    id = models.AutoField(auto_created = True, primary_key = True, serialize = False, verbose_name ='ID' )  
    userid = models.ForeignKey(User, on_delete = models.CASCADE)
    channelid = models.ForeignKey(Channel, on_delete= models.CASCADE)
    body = models.CharField(max_length=800)
    messageid = models.CharField(max_length=300)
    contenttype = models.CharField(max_length=300)
    teamid = models.ForeignKey(Team, on_delete = models.CASCADE)

    def __str__(self):
        return self.body

class FeedbackUpload(models.Model): 
    id = models.AutoField(auto_created = True, primary_key = True, serialize = False, verbose_name ='ID' ) 
    teamid  = models.ForeignKey(Team, on_delete = models.CASCADE)
    feedbackGivenPdf = models.BooleanField()

class Upload(models.Model):
    id = models.AutoField(auto_created = True, primary_key = True, serialize = False, verbose_name ='ID' ) 
    fileid = models.CharField(max_length=200, unique=True)
    teamid = models.ForeignKey(Team, on_delete = models.CASCADE)
    uploaddate = models.DateTimeField(null=True, blank=True)
    filename = models.CharField(max_length=200)

class Reminder(models.Model): 
    id = models.AutoField(auto_created = True, primary_key = True, serialize = False, verbose_name ='ID' ) 
    teamid = models.ForeignKey(Team, on_delete = models.CASCADE)
    triggerdate = models.DateTimeField(null=True, blank=True)
    subject = models.CharField(max_length=200)
    body = models.CharField(max_length=800)
