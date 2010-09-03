from oembed import DefaultOEmbedConsumer, OEmbedError

from django import forms
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from metaphore.models import *

from metaphore import settings

def make_unique_slug(queryset, value, slug_field='slug'):
    new_slug = orig_slug = slugify(value)

    # Make the slug unique
    count = 0
    while queryset.filter(**{slug_field: new_slug}).exists():
        count += 1
        logging.debug('Slug %s taken, trying next alternative' % new_slug)
        new_slug = u'%s-%d' % (orig_slug, count)

    return new_slug


class OembedAddForm(forms.ModelForm):
    """Form for Link"""

    class Meta:
        fields = ('url', )

    def clean(self, *args, **kwargs):
        if 'url' in self.cleaned_data:
            url = self.cleaned_data['url']
            try:
                params = {}
                
                if settings.OEMBED_MAX_WIDTH:
                    params.update({'maxwidth': settings.OEMBED_MAX_WIDTH})
                    
                if settings.OEMBED_MAX_HEIGHT:
                    params.update({'maxheight': settings.OEMBED_MAX_HEIGHT})

                response = DefaultOEmbedConsumer.embed(url, **params)

                logging.debug('Found OEmbed info for %s' % url)
                for field in response:
                    if hasattr(self.instance, field) and \
                            not getattr(self.instance, field):
                        logging.debug('Setting field %s: %s' \
                                        % (field, response[field]))
                        setattr(self.instance, field, response[field])

                        # If we set the title, also set the slug
                        if field == 'title' and not self.instance.slug:
                            logging.debug('Setting title with slug')
                            
                            self.instance.slug = \
                                make_unique_slug(Post.objects.all(), \
                                                 response['title'])

            except OEmbedError, e:
                logging.warn('Something went wrong with OEmbed: %s' % e)

                raise forms.ValidationError(_('Something went wrong looking \
                    up embed information for this URL: %s') % e)

        return super(OembedAddForm, self).clean(*args, **kwargs)


class EmbeddedVideoAddForm(OembedAddForm):
    class Meta(OembedAddForm.Meta):
        model = EmbeddedVideo


class EmbeddedPhotoAddForm(OembedAddForm):
    class Meta(OembedAddForm.Meta):
        model = EmbeddedPhoto


class EmbeddedRichAddForm(OembedAddForm):
    class Meta(OembedAddForm.Meta):
        model = EmbeddedRich


class LinkAddForm(OembedAddForm):
    class Meta(OembedAddForm.Meta):
        model = Link
