from django.db import models

from basemodels import PostAbstractBase

class Article(PostAbstractBase):
    text = models.TextField()

class Download(PostAbstractBase):
    download = models.FileField(upload_to='downloads')

class OembedAbstractBase(PostAbstractBase):
    class Meta:
        abstract = True
    
    url = models.URLField(verify_exists=True)
    
    def save(self, *args, **kwargs):
        
        super(self, OembedAbstractBase).save(*args, **kwargs)
    
class Link(OembedAbstractBase):
    pass

class EmbeddedVideo(OembedAbstractBase):
    html = models.TextField()
    width = models.SmallIntegerField(blank=True, null=True)
    height = models.SmallIntegerField(blank=True, null=True)
    
    thumbnail_url = models.URLField(blank=True, verify_exists=True)
    thumbnail_width = models.SmallIntegerField(blank=True, null=True)
    thumbnail_height = models.SmallIntegerField(blank=True, null=True)
    
    author_name = models.CharField(blank=True, max_length=255)
    author_url = models.URLField(blank=True, verify_exists=False)
    
    duration = models.SmallIntegerField(blank=True, null=True)
    
