from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
# Models available from the API
from django.contrib.auth.models import User
from jquest.models import *

class InstanceResource(ModelResource):    
    class Meta:    
        queryset = Instance.objects.all()
        resource_name = 'instance'
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class MissionResource(ModelResource):
    instance = fields.ForeignKey(InstanceResource, 'instance')
    class Meta:
        queryset = Mission.objects.all()
        resource_name = 'mission'
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class MissionRelationshipResource(ModelResource):
    class Meta:
        queryset = MissionRelationship.objects.all()
        resource_name = 'missionRelationship'
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class LanguageResource(ModelResource):
    class Meta:
        queryset = Language.objects.all()
        resource_name = 'language'
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class PostResource(ModelResource):
    class Meta:
        queryset = Post.objects.all()
        resource_name = 'post'
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class UserResource(ModelResource):
    class Meta:
        excludes = ("password", "last_login", "email")
        queryset = User.objects.all()
        resource_name = 'user'
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class UserOauthResource(ModelResource):
    class Meta:
        queryset = UserOauth.objects.all()
        resource_name = 'userOauth'
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class UserProgressionResource(ModelResource):
    class Meta:
        queryset = UserProgression.objects.all()
        resource_name = 'userProgression'
        
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()