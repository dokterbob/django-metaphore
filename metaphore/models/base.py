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
        return super(CurrentSiteManager, self).get_query_set().filter(publish=0, publish_date__lte=datetime.now())

class AssetManager(CurrentSiteManager):
    def get_query_set(self):
        return super(CurrentSiteManager, self).get_query_set().filter(publish=1)

class Post(models.Model):
    class Meta:
        get_latest_by = 'publish_date'
        ordering = ['-publish_date','-modify_date','-create_date']
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        permissions = (("change_author", ugettext("Change author")),)
        
        # A workaround for Ticket #4470
        app_label = 'metaphore'
        
    objects = models.Manager()
    on_site = CurrentSiteManager()
    published = PublicationManager()
    assets = AssetManager()
    
    title = models.CharField(max_length=255, verbose_name=_('title'))
    slug = models.SlugField(max_length=50, verbose_name=_('slug'), db_index=True)

    description = models.TextField(verbose_name=_('description'))

    author = models.ForeignKey(User, db_index=True)
    
    sites = models.ManyToManyField(Site, verbose_name=_('sites'), null=True, blank=True)

    # Overhere, a relationship to self is rather senseless - we ought to prevent it
    # Also, for some reason, changes do not get saved (anymore)
    # This is now officially a Django bug: ticket 8161
    links = models.ManyToManyField('self', verbose_name=_('links'), related_name='links', null=True, blank=True, symmetrical=True)

    PUBLISH_CHOICES = ((0, _('Publication')),
                       (1, _('Asset')),
                       (2, _('Hidden')))
    publish  = models.SmallIntegerField(verbose_name=_('type'), choices=PUBLISH_CHOICES, default=0)

    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('creation date'))
    modify_date = models.DateTimeField(auto_now=True, verbose_name=_('modification date'))
    publish_date = models.DateTimeField(verbose_name=_('publication date'), default=datetime.now(), null=True, blank=True)    
    
    content_type = models.ForeignKey(ContentType, editable=False)
    
    def content(self):
        return self.content_type.model_class().objects.get(post=self)
                
    def __unicode__(self):
        return u"%s %s" % (capfirst(self.content_type.model_class()._meta.verbose_name), self.title)  

# You might need the patch for ticket #7588 here.
class BasePost(Post):
    class Meta:
        abstract = True
        
        # A workaround for Ticket #4470
        app_label = 'metaphore'
    
    def __unicode__(self):
        return self.title
        
    post = models.OneToOneField('Post', parent_link=True, verbose_name=_('post'), editable=False, primary_key=True, db_index=True)

# This is not beautiful - but due to the limited number of Models the risk
# is limited, AFAIK.
from utils import _register_type
models.signals.class_prepared.connect(_register_type)