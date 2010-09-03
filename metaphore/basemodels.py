import logging

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, class_prepared
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import ping_google

from taggit.managers import TaggableManager

from metadata.models import TitleAbstractBase, SlugAbstractBase, \
                            AuthorAbstractBase, DescriptionAbstractBase, \
                            SitesPublicationAbstractBase, CommentsAbstractBase


class Post(TitleAbstractBase,
           SlugAbstractBase,
           AuthorAbstractBase,
           DescriptionAbstractBase,
           SitesPublicationAbstractBase,
           CommentsAbstractBase):

    class Meta(SitesPublicationAbstractBase.Meta):
        verbose_name = _('post')
        verbose_name_plural = _('posts')

        unique_together = ('slug', 'publish_date')

        permissions = (("change_author", ugettext("Change author")), )

    content_type = models.ForeignKey(ContentType, editable=False)
    links = models.ManyToManyField('self', verbose_name=_('related posts'), \
                                   related_name='links', null=True, \
                                   blank=True, symmetrical=True)
    tags = TaggableManager()


    @models.permalink
    def get_absolute_url(self):
        param_dict = {'year': self.publish_date.year,
                      'month': self.publish_date.month,
                      'day': self.publish_date.day,
                      'slug': self.slug}

        return ('metaphore-object-detail', (), param_dict)

    def content(self):
        # Do some primitive caching of the content object
        if hasattr(self, '_content'):
            return self._content
        else:
            model_class = self.content_type.model_class()
            self._content = model_class.objects.get(post=self)
            return self.content()

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if not settings.DEBUG:
            try:
                ping_google()
            except Exception:
                # Bare 'except' because we could get a variety
                # of HTTP-related exceptions.
                logging.warning('Error pinging Google while saving %s.' \
                                    % self)
        else:
            logging.debug('Not pinging Google while saving %s, DEBUG=True.' \
                            % self)



def _pre_save(sender, instance, **kwargs):
    ct = ContentType.objects.get_for_model(sender)
    instance.content_type = ct


class PostAbstractBase(Post):
    """ Abstract base class for actual post types; the stuff that actually
       gets posted on the website should inherit from this little critter. """

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(PostAbstractBase, self).__init__(*args, **kwargs)
        pre_save.connect(_pre_save, sender=self.__class__)

    post = models.OneToOneField('Post', parent_link=True, editable=False,
                                primary_key=True, db_index=True)
