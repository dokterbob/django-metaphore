from django.db import models

from basemodels import PostAbstractBase

class Article(PostAbstractBase):
    text = models.TextField()

class Download(PostAbstractBase):
    download = models.FileField(upload_to='downloads')

class Link(PostAbstractBase):
    url = models.URLField(verify_exists=True)
