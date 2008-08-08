from django.contrib import admin
from models import *

from django.utils.translation import ugettext as _

from django import forms

def get_default_sites():
    try:
        return [Site.objects.get_current()]
    except Exception:
        return []

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_create','date_modify', 'publish', 'date_publish')
    list_filter = ('publish', 'date_modify','date_publish', 'site')
    ordering = ('title',)
    
    prepopulated_fields = {'slug':('title',)}
 
    #filter_horizontal = ('links',)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "site": # Check if it's the one you want
            kwargs.update({'initial': get_default_sites()})
            
        return super(PostAdmin, self).formfield_for_dbfield(db_field, **kwargs) # Get the default field
            
    def get_fieldsets(self, request, obj=None):
        fieldsets_orig = super(PostAdmin, self).get_fieldsets(request, obj)
        
        post_fields = ['title','slug']
        
        # Only superusers can change authors, for now
        if request.user.has_perm('change_author'):
            post_fields.append('author')
            
        post_fields += ['description', 'site', 'publish', 'date_publish']
            
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
    def add_view(self, request, *args, **kwargs):
          if request.method == "POST":
              # If we DO NOT have change permissions, make sure we override the author to the current user
              if not request.user.has_perm('change_author'):
                  postdict = request.POST.copy()
                  postdict['author'] = request.user.id
                  request.POST = postdict
                  
          elif not request.GET.has_key('author'):
              # We are handling a GET, we default to current user
              getdict = request.GET.copy()
              getdict['author'] = request.user.id
              request.GET = getdict
                              
          return super(PostAdmin, self).add_view(request, *args, **kwargs)
     
          def change_view(self, request, *args, **kwargs):
              if request.method == "POST":
                  # If we DO NOT have change permissions, make sure we override the author to the current user
                  if not request.user.has_perm('change_author'):
                      postdict = request.POST.copy()
                      postdict['author'] = request.user.id
                      request.POST = postdict
                      
              return super(PostAdmin, self).change_view(request, *args, **kwargs)

    #blank = ('date_publish', 'links')
    #date_hierarchy = 'date_publish'

admin.site.register(Article, PostAdmin)
admin.site.register(Download, PostAdmin)
