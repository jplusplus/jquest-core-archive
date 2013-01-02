from django.conf.urls import patterns, include, url
from django.contrib import admin
# Models available from the API
from jquest.api import *

admin.autodiscover()

instance_resource = InstanceResource()
mission_resource = MissionResource()
missionrelationship_resource = MissionRelationshipResource()
user_resource = UserResource()
useroauth_resource = UserOauthResource()
userprogression_resource = UserProgressionResource()
post_resource = PostResource()
language_resource = LanguageResource()

API_ROOT = ""

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls) ),
    url(r'^grappelli/',include('grappelli.urls') ),
    (API_ROOT, include(instance_resource.urls) ),
    (API_ROOT, include(mission_resource.urls) ),
    (API_ROOT, include(missionrelationship_resource.urls) ),
    (API_ROOT, include(user_resource.urls) ),
    (API_ROOT, include(useroauth_resource.urls) ),
    (API_ROOT, include(userprogression_resource.urls) ),
    (API_ROOT, include(post_resource.urls) ),
    (API_ROOT, include(language_resource.urls) )
)








