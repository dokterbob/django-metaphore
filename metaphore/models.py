from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from django.utils.html import strip_tags

from django.utils.text import capfirst

from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.contrib.auth.models import User

from datetime import datetime

class PublicationManager(CurrentSiteManager):
    def get_query_set(self):
        return super(CurrentSiteManager, self).get_query_set().filter(publish=True, date_publish__lte=datetime.now())

class Post(models.Model):
    class Meta:
        get_latest_by = 'date_publish'
        ordering = ['-date_publish','-date_modify','-date_create']
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        permissions = (("change_author", ugettext("Change author")),)
        
    objects = models.Manager()
    on_site = CurrentSiteManager()
    published = PublicationManager()
    
    title = models.CharField(max_length=255, verbose_name=_('title'))
    slug = models.SlugField(max_length=50, verbose_name=_('slug'), db_index=True)

    description = models.TextField(verbose_name=_('description'))

    author = models.ForeignKey(User)
    
    site = models.ManyToManyField(Site, verbose_name=_('sites'), null=True, blank=True)

    # Overhere, a relationship to self is rather senseless - we ought to prevent it
    # Also, for some reason, changes do not get saved (anymore)
    # This is now officially a Django bug: ticket 8161
    links = models.ManyToManyField('self', verbose_name=_('links'), related_name='links', null=True, blank=True, symmetrical=True)

    date_create = models.DateTimeField(auto_now_add=True, verbose_name=_('creation date'))
    date_modify = models.DateTimeField(auto_now=True, verbose_name=_('modification date'))
    date_publish = models.DateTimeField(verbose_name=_('publication date'), null=True, blank=True)
    
    publish = models.BooleanField(verbose_name=_('publish'), default=False)
    
    content_type = models.ForeignKey(ContentType, editable=False)
    
    def content(self):
        return self.content_type.model_class().objects.get(post=self)
                
    def __unicode__(self):
        return u"%s %s" % (capfirst(self.content_type.model_class()._meta.verbose_name), self.title)  
    
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

