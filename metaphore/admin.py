from django.contrib import admin

from baseadmin import PostAdmin
from models import *
    
class ArticleAdmin(PostAdmin):
    pass

admin.site.register(Article, ArticleAdmin)

class DownloadAdmin(PostAdmin):
    pass

admin.site.register(Download, DownloadAdmin)
