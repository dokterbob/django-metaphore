from oembed import DefaultOEmbedConsumer, OEmbedError

from django import forms

from django.template.defaultfilters import slugify     

from models import *

from django.conf import settings
OEMBED_WIDTH = getattr(settings, 'OEMBED_WIDTH', None)
OEMBED_HEIGHT = getattr(settings, 'OEMBED_HEIGHT', None)

opt = {}
if OEMBED_WIDTH:
    opt.update({'width':int(OEMBED_WIDTH)})
if OEMBED_HEIGHT:
    opt.update({'height':int(OEMBED_HEIGHT)})

class OembedAddForm(forms.ModelForm):
    """Form for Link"""
    
    class Meta:
        fields = ('url', )

    def clean(self, *args, **kwargs):
        if self.cleaned_data.has_key('url'):
            url = self.cleaned_data['url']
            try:
                response = DefaultOEmbedConsumer.embed(url, **opt)
                logging.debug('Found OEmbed info for %s' % url)            
                for field in response:
                    if hasattr(self.instance, field) and \
                            not getattr(self.instance, field):
                        logging.debug('Setting field %s: %s' \
                                        % (field, response[field]))
                        setattr(self.instance, field, response[field])
                    
                        # If we set the title, also set the slug
                        if field == 'title' and \
                                not getattr(self.instance, 'slug'):
                            logging.debug('Setting title with slug')
                            orig_slug = title_slug = \
                                slugify(response['title'])
                        
                            # Make the slug unique
                            count = 0
                            while Post.objects.filter(slug=title_slug).count():
                                count += 1
                                logging.debug('Slug %s taken, trying next  alternative'\
                                                % title_slug)
                                title_slug = u'%s-%d' % (orig_slug, count)
                        
                            setattr(self.instance, 'slug', title_slug)
            except OEmbedError, e:
                logging.warn('Something went wrong with OEmbed: %s' % e)
                raise forms.ValidationError('Something went wrong looking up embed  information for this URL: %s' % e)
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