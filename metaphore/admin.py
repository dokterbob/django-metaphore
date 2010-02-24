from django.contrib import admin

from baseadmin import PostAdmin
from models import *
    
class ArticleAdmin(PostAdmin):
    pass

admin.site.register(Article, ArticleAdmin)

class DownloadAdmin(PostAdmin):
    pass

admin.site.register(Download, DownloadAdmin)

class LinkAdmin(PostAdmin):
    pass

admin.site.register(Link, LinkAdmin)

class EmbeddedVideoAdmin(PostAdmin):
    pass

admin.site.register(EmbeddedVideo, EmbeddedVideoAdmin)

class EmbeddedPhotoAdmin(PostAdmin):
    pass

admin.site.register(EmbeddedPhoto, EmbeddedPhotoAdmin)

class EmbeddedRichAdmin(PostAdmin):
    pass

admin.site.register(EmbeddedRich, EmbeddedRichAdmin)
