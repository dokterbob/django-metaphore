import logging

from django.contrib import admin

from metaphore.baseadmin import PostAdmin
from metaphore.models import *
from metaphore.forms import * 

if settings.USE_TINYMCE:
    from tinymce.widgets import TinyMCE
    
class ArticleAdmin(PostAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if settings.USE_TINYMCE and db_field.name == 'text':
            kwargs['widget'] = TinyMCE
        return super(ArticleAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Article, ArticleAdmin)

class DownloadAdmin(PostAdmin):
    pass

admin.site.register(Download, DownloadAdmin)

class OembedAdmin(PostAdmin):
    prepopulated_fields = {}
        
    def save_model(self, request, obj, form, change):
        if not change:
            # We're making a new object here and should set decent default
            # values for author and sites
            logging.debug('New oembed object. Settings default author')
            
            obj.author = request.user
                
        super(OembedAdmin, self).save_model(request, obj, form, change)
        
        if not change:
            logging.debug('New oembed object. Settings default sites')

            from django.contrib.sites.models import Site
            obj.sites = Site.objects.all()
    
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
