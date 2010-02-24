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
        
        response = DefaultOEmbedConsumer.embed(self.url)
        
        for field in response:
            if hasattr(self, field) and getattr(self, field) == None:
                self.field = response[field]
        
        super(OembedAbstractBase, self).save(*args, **kwargs)
    
class Link(OembedAbstractBase):
    pass

class EmbeddedRich(OembedAbstractBase):
    html = models.TextField()
    width = models.SmallIntegerField(blank=True, null=True)
    height = models.SmallIntegerField(blank=True, null=True)

class EmbeddedVideo(EmbeddedRich):        
    duration = models.SmallIntegerField(blank=True, null=True)
    
class EmbeddedPhoto(OembedAbstractBase):
    width = models.SmallIntegerField(blank=True, null=True)
    height = models.SmallIntegerField(blank=True, null=True)
    
