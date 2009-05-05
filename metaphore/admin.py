from django.contrib import admin
#from django.contrib.sites.models import Site

from django.utils.translation import ugettext as _

from django import forms
from django.forms.models import modelform_factory

from models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_date','modify_date', 'publish', 'publish_date')
    list_filter = ('publish', 'modify_date','publish_date', 'sites')
    ordering = ('title',)
    search_fields = ('title', 'slug', 'description')
    
    actions_on_top = False
    actions_on_bottom = True
    
    prepopulated_fields = {'slug':('title',)}
    
    date_hierarchy = 'publish_date'
    
    def get_fieldsets(self, request, obj=None):
        base_fieldset =     (_('General'),
                             {'fields' : ('title', 'slug', 'description')})
        advanced_fieldset = (_('Advanced options'),
                             {'classes': ('collapse',),
                              'fields' : ('publish', 'publish_date','publish_time', 'sites','allow_comments')})
        #related_fieldset =  (_('Links'), 
        #                     {'classes': ('collapse',),
        #                      'fields': ('links',)})#

        # If we're not allowed to change the author, remove that one from the post fields       
        if request.user.has_perm('change_author'):
            advanced_fieldset[1]['fields'] = ('author',) + advanced_fieldset[1]['fields']

        # Get all fields for the currend model
        fieldsets_orig = super(PostAdmin, self).get_fieldsets(request, obj)
        fields_orig = fieldsets_orig[0][1]['fields']

        # Remove common fieldsets from the total of all fields
        fields_new = base_fieldset[1]['fields'] + advanced_fieldset[1]['fields'] #+ related_fieldset[1]['fields']

        for field in fields_new:
            if field in fields_orig:
                fields_orig.remove(field)

        content_fieldset = (_('Content'),  
                           {'fields': fields_orig })

        fieldsets = (base_fieldset, advanced_fieldset, content_fieldset ) #related_fieldset
        return fieldsets

    def has_change_permission(self, request, obj=None):
        """ Make sure a user can only edit it's own entries. """

        if not obj:
            return True

        if obj.author == request.user:
            return True

        if request.user.is_superuser:
            return True

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

    # there are hooks for this user stuff nowadays
    def change_view(self, request, *args, **kwargs):
        if request.method == "POST":
            # If we DO NOT have change permissions, make sure we override the author to the current user
            if not request.user.has_perm('change_author'):
                postdict = request.POST.copy()
                postdict['author'] = request.user.id
                request.POST = postdict

        return super(PostAdmin, self).change_view(request, *args, **kwargs)
    
class ArticleAdmin(PostAdmin):
    pass

admin.site.register(Article, ArticleAdmin)

class DownloadAdmin(PostAdmin):
    pass

admin.site.register(Download, DownloadAdmin)
