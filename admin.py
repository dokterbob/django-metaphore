from django.contrib import admin
from models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_create','date_modify','publish', 'date_publish')
    list_filter = ('publish', 'date_modify','date_publish')
    ordering = ('title',)
    #blank = ('date_publish', 'links')
    #date_hierarchy = 'date_publish'
    