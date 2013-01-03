# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.sites.models import Site
from datetime import datetime
from jquest.models import *

class MissionInline(admin.StackedInline):
    model = Mission
    extra = 9

class InstanceAdmin(admin.ModelAdmin):
    list_display = ("name","id")
    inlines = (MissionInline,)

class MissionAdmin(admin.ModelAdmin):
    search_fields  = ("name","instance")
    list_display = ("name","instance", "id")
    
class LanguageAdmin(admin.ModelAdmin):
    pass
class PostAdmin(admin.ModelAdmin):
    pass    
class UserOauthAdmin(admin.ModelAdmin):
    pass
class UserProgressionAdmin(admin.ModelAdmin):
    list_display = ("id","user","mission")
    pass

# Register all models in admin
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Mission, MissionAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserOauth, UserOauthAdmin)
admin.site.register(UserProgression, UserProgressionAdmin)

# Disable "Site" in the admin panel 
admin.site.unregister(Site)
