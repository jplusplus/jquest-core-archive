from django.db import models
from django.contrib.auth.models import User

class Instance(models.Model):
    name = models.CharField(max_length=135)
    host = models.CharField(max_length=135)
    slug = models.CharField(max_length=135, blank=True)
    
    def __unicode__(self):
        return self.name

class Mission(models.Model):
    instance = models.ForeignKey(Instance, null=True, db_column='instance', blank=True)
    name = models.CharField(max_length=135, blank=True)

    def __unicode__(self):
        return str(self.instance) + ": " + self.name

class MissionRelationship(models.Model):
    mission = models.ForeignKey(Mission, null=True, db_column='mission', blank=True, related_name='+')
    parent = models.ForeignKey(Mission, null=True, db_column='parent', blank=True, related_name='+')

class Language(models.Model):
    code = models.CharField(max_length=24, primary_key=True)
    name = models.CharField(max_length=135, blank=True)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=768, blank=True)
    excerpt = models.CharField(max_length=1536, blank=True)
    content = models.TextField(blank=True)
    createdat = models.DateTimeField(null=True, db_column='createdAt', blank=True) # Field name made lowercase.
    language = models.ForeignKey(Language, null=True, db_column='language', blank=True)
    
    def __unicode__(self):
        return self.title
  
class UserOauth(models.Model):
    consumer = models.CharField(max_length=765, blank=True)
    consumeruserid = models.IntegerField(null=True, db_column='consumerUserId', blank=True) # Field name made lowercase.
    oauthaccesstoken = models.CharField(max_length=765, db_column='oauthAccessToken', blank=True) # Field name made lowercase.
    oauthaccesstokensecret = models.CharField(max_length=765, db_column='oauthAccessTokenSecret', blank=True) # Field name made lowercase.
    user = models.ForeignKey(User, null=True, db_column='user', blank=True)

    def __unicode__(self):
        return self.user

class UserProgression(models.Model):
    mission = models.ForeignKey(Mission, null=True, db_column='mission', blank=True)
    user = models.ForeignKey(User, null=True, db_column='user', blank=True)
    points = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=765, blank=True)    
