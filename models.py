from django.db import models

from django.utils.translation import ugettext_lazy as _

from django.utils.html import strip_tags

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from datetime import datetime

class Post(models.Model):
    class Meta:
        get_latest_by = 'date_publish'
        ordering = ['-date_publish','-date_modify','-date_create']
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    
    links = models.ManyToManyField('self', verbose_name=_('links'), null=True, blank=True, related_name='links')

    date_create = models.DateTimeField(auto_now_add=True, verbose_name=_('creation date'))
    date_modify = models.DateTimeField(auto_now=True, verbose_name=_('modification date'))
    date_publish = models.DateTimeField(verbose_name=_('publication date'), null=True, blank=True)
    
    publish = models.BooleanField(verbose_name=_('publish'), default=False)
    
    content_type = models.ForeignKey(ContentType, editable=False)

    # a author (User) belongs here as well
    
    def save(self):
        if self.publish and not self.date_publish:
            self.date_publish = datetime.now()
            
        super(Post, self).save()
    
    def content(self):
        return self.content_type.model_class().objects.get(post=self)

    def render_html(self):
        self.content().render_html()
        
    def render_text(self):
        # Check for special text function
        content = self.content()
        if hasattr(content, 'render_text'):
            return content.render_text()
        
        # Otherwise resort to stripped HTML
        return strip_tags(content.render_html())
        
    def __unicode__(self):
        return u"%s %s" % (self.content_type.model_class()._meta.verbose_name, self.title)  

class BasePost(models.Model):
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.title
        
class Article(Post, BasePost):
    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        
    post = models.OneToOneField('Post', parent_link=True, verbose_name=_('post'), editable=False, primary_key=True, db_index=True)

    def save(self):
        self.content_type = ContentType.objects.get_for_model(Article)
        super(Article, self).save()
        
    text = models.TextField(verbose_name=_('text'))

class Download(Post, BasePost):
    class Meta:
        verbose_name = _('download')
        verbose_name_plural = _('downloads')
        
    post = models.OneToOneField('Post', parent_link=True, verbose_name=_('post'), editable=False, primary_key=True, db_index=True)

    def save(self):
        self.content_type = ContentType.objects.get_for_model(Download)
        super(Download, self).save()

    filename = models.FileField(verbose_name=_('filename'), upload_to='downloads')    

from admin import *
from django.contrib import admin
admin.site.register(Article, PostAdmin)
admin.site.register(Download, PostAdmin)
