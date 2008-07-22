from django.db import models

from django.utils.translation import ugettext_lazy as _

from django.utils.html import strip_tags

from django.utils.text import capfirst

from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.contrib.auth.models import User

from datetime import datetime

def get_default_sites():
    try:
        return [Site.objects.get_current()]
    except Exception:
        return []

class Post(models.Model):
    class Meta:
        get_latest_by = 'date_publish'
        ordering = ['-date_publish','-date_modify','-date_create']
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        permissions = (("change_author", _("Change author")),)
        
    objects = models.Manager()
    on_site = CurrentSiteManager()
        
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))

    author = models.ForeignKey(User)
    
    site = models.ManyToManyField(Site, default=get_default_sites())

    # Overhere, a relationship to self is rather senseless - we ought to prevent it
    # Also, for some reason, changes do not get saved (anymore)
    links = models.ManyToManyField('self', verbose_name=_('links'), null=True, blank=True, related_name='links')

    date_create = models.DateTimeField(auto_now_add=True, verbose_name=_('creation date'))
    date_modify = models.DateTimeField(auto_now=True, verbose_name=_('modification date'))
    date_publish = models.DateTimeField(verbose_name=_('publication date'), null=True, blank=True)
    
    publish = models.BooleanField(verbose_name=_('publish'), default=False)
    
    content_type = models.ForeignKey(ContentType, editable=False)

    def save(self):
        if self.publish and not self.date_publish:
            self.date_publish = datetime.now()
                    
        super(Post, self).save()
    
    def content(self):
        return self.content_type.model_class().objects.get(post=self)

    # This does not belong in here according to DRY
    # But this way is definitly the easiest
    def render(self, format='html'):
        self.content().render(format)
                
    def __unicode__(self):
        return u"%s %s" % (capfirst(self.content_type.model_class()._meta.verbose_name), self.title)  
    
    # We should create a custom manager for this. TBD
    @classmethod
    def published(self):
        Post.on_site.filter(published=True, date_publish__lte=datetime.now())
        
from django.template.loader import get_template, select_template
# Somehow, generic relations do not seem to work here
# Workaround needed to link back to Post as we do in this BaseClass's subclasses
class BasePost(models.Model):
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.title
        
    def render(self, format='html'):
        template = get_template('post/render/post.%s' % format)
    
        context = Context({'post': self})
        
        print 'Rendering %s, %s' % (self, self.__class__)
        
        return template.render(context)
        
class Article(Post, BasePost):
    # This part is generic and should be automated    
    post = models.OneToOneField('Post', parent_link=True, verbose_name=_('post'), editable=False, primary_key=True, db_index=True)

    def save(self):
        self.content_type = ContentType.objects.get_for_model(Article)
        super(Article, self).save()        
    # End of generic part

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
    
    text = models.TextField(verbose_name=_('text'))

class Download(Post, BasePost):
    # This part is generic and should be automated    
    post = models.OneToOneField('Post', parent_link=True, verbose_name=_('post'), editable=False, primary_key=True, db_index=True)

    def save(self):
        self.content_type = ContentType.objects.get_for_model(Download)
        super(Download, self).save()
    # End of generic part

    class Meta:
        verbose_name = _('download')
        verbose_name_plural = _('downloads')
    
    filename = models.FileField(verbose_name=_('filename'), upload_to='downloads')    

from admin import *
from django.contrib import admin
admin.site.register(Article, PostAdmin)
admin.site.register(Download, PostAdmin)
