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

"""
class ReponseInline(admin.StackedInline):
  model = Reponse
  extra = 3

class SondageAdmin(admin.ModelAdmin):
  fields         = ('question', 'family')
  list_display   = ('id','question','was_published_today')
  inlines        = (ReponseInline,)
  search_fields  = ("question",)
  date_hierarchy = ("date_publication")

  def was_published_today(a, self):
    return self.date_publication.date() == datetime.date.today()
  was_published_today.short_description = u'Publié aujourd\'hui ?'

admin.site.register(Sondage, SondageAdmin)

class ReponseAdmin(admin.ModelAdmin):
  list_display = ('id','choix','sondage')

admin.site.register(Reponse, ReponseAdmin)
"""