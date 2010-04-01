import logging

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, class_prepared
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import ping_google

from metadata.models import MetaDataAbstractBase

class Post(MetaDataAbstractBase):
    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        
        unique_together = ('slug', 'publish_date')
    
    content_type = models.ForeignKey(ContentType, editable=False)
        
    @models.permalink
    def get_absolute_url(self):
        param_dict = { 'year'  : self.publish_date.year,
                       'month' : self.publish_date.month,
                       'day'   : self.publish_date.day,
                       'slug'  : self.slug }

        return ('metaphore-object-detail', (), param_dict)

    def content(self):
        if hasattr(self, '_content'):
            return self._content
        else:
            self._content = self.content_type.model_class().objects.get(post=self)
            return self.content()
    
    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if not settings.DEBUG:
            try:
                ping_google()
            except Exception:
                # Bare 'except' because we could get a variety
                # of HTTP-related exceptions.
                logging.warning('Error pinging Goole while saving %s.' % self)
        else:
            logging.debug('Not pinging Google while saving %s because DEBUG=True.' % self)
        

def _pre_save(sender, instance, **kwargs):
    ct = ContentType.objects.get_for_model(sender)
    instance.content_type = ct    

class PostAbstractBase(Post):
    class Meta:
        abstract = True
        ordering = ['-publish_date', '-publish_time']
        get_latest_by = 'publish_date'
    
    def __init__(self, *args, **kwargs):
        super(PostAbstractBase, self).__init__(*args, **kwargs)
        pre_save.connect(_pre_save, sender=self.__class__)
    
    post = models.OneToOneField('Post', parent_link=True, editable=False, primary_key=True, db_index=True)