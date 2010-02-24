import logging

from django.db import models

from basemodels import Post, PostAbstractBase

class Article(PostAbstractBase):
    text = models.TextField()

class Download(PostAbstractBase):
    download = models.FileField(upload_to='downloads')

class OembedAbstractBase(PostAbstractBase):
    class Meta:
        abstract = True
    
    # Title is already in there
    
    url = models.URLField(verify_exists=True)
    
    thumbnail_url = models.URLField(blank=True, verify_exists=True)
    thumbnail_width = models.SmallIntegerField(blank=True, null=True)
    thumbnail_height = models.SmallIntegerField(blank=True, null=True)

    provider_name = models.CharField(blank=True, max_length=255)
    provider_url = models.CharField(blank=True, max_length=255)
    
    author_name = models.CharField(blank=True, max_length=255)
    author_url = models.URLField(blank=True, verify_exists=False)

    def save(self, *args, **kwargs):
        from oembed import DefaultOEmbedConsumer        
        
        try:
            response = DefaultOEmbedConsumer.embed(self.url)
            logging.debug('Found OEmbed info for %s' % self.url)            
            for field in response:
                if hasattr(self, field) and not getattr(self, field):
                    logging.debug('Setting field %s: %s' % (field, response[field]))
                    setattr(self, field, response[field])
        except Exception, e:
            logging.warn('Something went with OEmbed: %s' % e)
        
        super(OembedAbstractBase, self).save(*args, **kwargs)
    
class Link(OembedAbstractBase):
    pass

class EmbeddedRich(OembedAbstractBase):
    html = models.TextField()
    width = models.SmallIntegerField(blank=True, null=True)
    height = models.SmallIntegerField(blank=True, null=True)

class EmbeddedVideo(EmbeddedRich):        
    """
    >>> from datetime import datetime
    >>> from django.contrib.auth.models import User
    >>> a = User.objects.all()[0]
    >>> now = datetime.now()
    >>> v = EmbeddedVideo()
    >>> v.slug = 'bogusslug'+str(now.date())+str(now.microsecond)
    >>> v.publish_date = now
    >>> v.author = a
    >>> v.url = 'http://www.vimeo.com/9683140'
    >>> v.save()
    >>> v.duration
    '891'
    >>> v.title
    'the earth in the air [a short film]'
    >>> v.url
    'http://www.vimeo.com/9683140'
    >>> v.thumbnail_url 
    'http://ts.vimeo.com.s3.amazonaws.com/486/494/48649497_200.jpg'
    """
    duration = models.SmallIntegerField(blank=True, null=True)
    
class EmbeddedPhoto(OembedAbstractBase):
    width = models.SmallIntegerField(blank=True, null=True)
    height = models.SmallIntegerField(blank=True, null=True)
    
