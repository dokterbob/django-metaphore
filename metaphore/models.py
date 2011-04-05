from sorl.thumbnail import ImageField

import logging

from django.db import models

from basemodels import Post, PostAbstractBase

from images.models import Image


class Article(PostAbstractBase):
    text = models.TextField()
    images = models.ManyToManyField(Image, blank=True, null=True, verbose_name='afbeeldingen')


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


class Link(OembedAbstractBase):
    pass


class EmbeddedRich(OembedAbstractBase):
    html = models.TextField(blank=True)
    width = models.SmallIntegerField(blank=True, null=True)
    height = models.SmallIntegerField(blank=True, null=True)


class EmbeddedVideo(OembedAbstractBase):
    html = models.TextField(blank=True)
    width = models.SmallIntegerField(blank=True, null=True)
    height = models.SmallIntegerField(blank=True, null=True)

    duration = models.SmallIntegerField(blank=True, null=True)


class EmbeddedPhoto(OembedAbstractBase):
    width = models.SmallIntegerField(blank=True, null=True)
    height = models.SmallIntegerField(blank=True, null=True)


class Photo(PostAbstractBase):
    photo = ImageField(upload_to='metaphore_images')