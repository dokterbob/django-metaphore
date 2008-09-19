from django.contrib import admin
from django.contrib.sites.models import Site

from django.utils.translation import ugettext as _

from django import forms
from django.forms.models import modelform_factory

from models.base import Post

def get_default_sites():
    try:
        return Site.objects.all()
    except Exception:
        return []

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_create','date_modify', 'publish', 'date_publish')
    list_filter = ('publish', 'date_modify','date_publish', 'site')
    ordering = ('title',)
    search_fields = ('title', 'slug', 'description')
    
    prepopulated_fields = {'slug':('title',)}
    
    date_hierarchy = 'date_publish'
     
    if 'links' in modelform_factory(Post).base_fields.keys():
        filter_horizontal = ('links',)
    
    # This is a dirty hack, this belongs inside of the model but defaults don't work on M2M
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "site": # Check if it's the one you want
            kwargs.update({'initial': [Site.objects.get_current()]})
            
        return super(PostAdmin, self).formfield_for_dbfield(db_field, **kwargs) # Get the default field
            
    def get_fieldsets(self, request, obj=None):
        # Get all the fields for post
        post_fields = modelform_factory(Post).base_fields.keys()
        
        # Get all fields for the currend model
        fieldsets_orig = super(PostAdmin, self).get_fieldsets(request, obj)
        fields_orig = fieldsets_orig[0][1]['fields']
        
        # First, remove all fields that belong to Post from the default list of fields
        for field in post_fields:
            if field in fields_orig:
                fields_orig.remove(field)
        
        # If we're not allowed to change the author, remove that one from the post fields       
        if  'author' in post_fields and not request.user.has_perm('change_author'):
            post_fields.remove('author')
        
        # Links belongs in it's own fieldset        
        if 'links' in post_fields:
            post_fields.remove('links')
            related_set = (_('Related posts'), {'fields': ['links',]}) 
        else:
            related_set = None
        
        # Put all post-fields in a separate formset
        fieldsets = [ (_('Post'), {'fields': post_fields }), ]
        
        # Add a formset for related objects, if the field's available
        fieldsets.append(related_set)
        
        # Appent the content fields in their own fieldset
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
            print 'DEBUG'
            print request.POST
            # If we DO NOT have change permissions, make sure we override the author to the current user
            if not request.user.has_perm('change_author'):
                postdict = request.POST.copy()
                postdict['author'] = request.user.id
                request.POST = postdict

        return super(PostAdmin, self).change_view(request, *args, **kwargs)
