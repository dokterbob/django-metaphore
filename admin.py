from django.contrib import admin
from models import *

from django.utils.translation import ugettext as _

import django.newforms as forms

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_create','date_modify', 'publish', 'date_publish')
    list_filter = ('publish', 'date_modify','date_publish', 'site')
    ordering = ('title',)
    #filter_vertical = ('links',)
    
    def get_fieldsets(self, request, obj=None):
        fieldsets_orig = super(PostAdmin, self).get_fieldsets(request, obj)
        
        post_fields = ['title',]
        
        # Only superusers can change authors, for now
        if request.user.has_perm('change_author'):
            post_fields.append('author')
            
        post_fields += ['description', 'site', 'date_publish', 'publish']
            
        fieldsets = [ (_('Post'), {'fields': post_fields }), ]
        
        fields_orig = fieldsets_orig[0][1]['fields']
        
        for field in post_fields:
            fields_orig.remove(field)
            
        # See above
        if 'author' in fields_orig:
            print 'Author removed'
            fields_orig.remove('author')
            
        fields_orig.remove('links')
        fieldsets.append( (_('Related posts'), {'fields': ['links',]}))
            
        fieldsets.append( (_('Content'),  {'fields': fields_orig }) )
        
        return fieldsets

    def has_change_permission(self, request, obj=None):
        """ Make sure a user can only edit it's own entries. """
        if not obj:
            return True
        
        if obj.author == request.user:
            return True
            
        if request.user.is_superuser:
            return True
            
        # There should also be a group of Metablog superusers.
        # TO-BE-DONE
            
        return False
   
    # A little hack found in http://django.freelancernepal.com/topics/django-newforms-admin/
    def add_view(self, request):
        if request.method == "POST":
            if not (request.user.has_perm('change_author') and request.POST.has_key('author') and len(request.POST['author'])):
                request.POST['author'] = request.user.id                
            
        return super(PostAdmin, self).add_view(request)

        def change_view(self, request):
            if request.method == "POST":
                if not (request.user.has_perm('change_author') and request.POST.has_key('author') and len(request.POST['author'])):
                    request.POST['author'] = request.user.id

            return super(PostAdmin, self).add_view(request)

    #blank = ('date_publish', 'links')
    #date_hierarchy = 'date_publish'
    