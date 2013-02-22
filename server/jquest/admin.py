# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.sites.models import Site
from datetime import datetime
from jquest.models import *

class MissionParentInline(admin.TabularInline):
    model = MissionRelationship
    fields = ("parent",)
    fk_name = "mission"
    extra = 1

class MissionInline(admin.TabularInline):
    model = Mission
    extra = 3

class InstanceAdmin(admin.ModelAdmin):
    list_display = ("name","id")
    inlines = (MissionInline,)

class MissionAdmin(admin.ModelAdmin):
    search_fields  = ("name","instance")
    list_display = ("name","instance", "id")    
    inlines = (MissionParentInline,)
    
class LanguageAdmin(admin.ModelAdmin):
    pass
class PostAdmin(admin.ModelAdmin):
    pass    
class UserOauthAdmin(admin.ModelAdmin):
    pass
class UserTokenAdmin(admin.ModelAdmin):
    pass
class UserProgressionAdmin(admin.ModelAdmin):    
    pass    
class EntityAdmin(admin.ModelAdmin):
    pass    
class EntityEvalAdmin(admin.ModelAdmin):
    pass    
class EntityFamilyAdmin(admin.ModelAdmin):
    pass    

# Register all models in admin
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Mission, MissionAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserOauth, UserOauthAdmin)
admin.site.register(UserToken, UserTokenAdmin)
admin.site.register(UserProgression, UserProgressionAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(EntityEval, EntityEvalAdmin)
admin.site.register(EntityFamily, EntityFamilyAdmin)

# Disable "Site" in the admin panel 
admin.site.unregister(Site)
