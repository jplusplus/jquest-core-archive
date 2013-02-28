from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
# Models available from the API
from jquest.api import *
from django.conf import settings

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(InstanceResource())
v1_api.register(MissionResource())
v1_api.register(MissionRelationshipResource())
v1_api.register(UserResource())
v1_api.register(UserOauthResource())
v1_api.register(UserTokenResource())
v1_api.register(UserProgressionResource())
v1_api.register(PostResource())
v1_api.register(EntityFamilyResource())
v1_api.register(EntityResource())
v1_api.register(EntityEvalResource())

urlpatterns = patterns('',
    # Admin documentor
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Admin dashboard
    url(r'^admin/', include(admin.site.urls) ),
    # Admin theme
    url(r'^grappelli/', include('grappelli.urls') ),
    # API documentor
    url(r'^v1/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
    # API resources    
    url('', include(v1_api.urls)),
    # Allow media access
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT
    }),
)








