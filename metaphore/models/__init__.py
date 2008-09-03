from base import Post

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base import BasePost

# Due to Ticket #4470 (to be fixed soon), the content types are limited
# to this file only.

class Article(BasePost):
    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    text = models.TextField(verbose_name=_('text'))

class Download(BasePost):
    class Meta:
        verbose_name = _('download')
        verbose_name_plural = _('downloads')

    download = models.FileField(verbose_name=_('filename'), upload_to='downloads')
