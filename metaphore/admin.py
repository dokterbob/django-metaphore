import logging

from django.contrib import admin

from baseadmin import PostAdmin
from models import *
from forms import * 
    
class ArticleAdmin(PostAdmin):
    pass

admin.site.register(Article, ArticleAdmin)

class DownloadAdmin(PostAdmin):
    pass

admin.site.register(Download, DownloadAdmin)

class OembedAdmin(PostAdmin):
    prepopulated_fields = {}
        
    def save_model(self, request, obj, form, change):
        if not obj.id or not obj.author:
            obj.author = request.user
            obj.save()
        
        super(OembedAdmin, self).save_model(request, obj, form, change)
    
    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            # We're adding stuff
            logging.debug('Rendering add form for %s' % self.model)
            return self.add_form
        else:
            logging.debug('Rendering normal form.')
            return super(OembedAdmin, self).get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return super(PostAdmin, self).get_fieldsets(request, obj)
        else:
            return super(OembedAdmin, self).get_fieldsets(request, obj)

class LinkAdmin(OembedAdmin):
    add_form = LinkAddForm
admin.site.register(Link, LinkAdmin)

class EmbeddedVideoAdmin(OembedAdmin):
    add_form = EmbeddedVideoAddForm

admin.site.register(EmbeddedVideo, EmbeddedVideoAdmin)

class EmbeddedPhotoAdmin(OembedAdmin):
    add_form = EmbeddedPhotoAddForm

admin.site.register(EmbeddedPhoto, EmbeddedPhotoAdmin)

class EmbeddedRichAdmin(OembedAdmin):
    add_form = EmbeddedRichAddForm

admin.site.register(EmbeddedRich, EmbeddedRichAdmin)
