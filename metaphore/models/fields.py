from tinymce.widgets import TinyMCE
from django.db import models

class HTMLField(models.TextField):
    def __init__(self, *args, **kwargs):
        return super(HTMLField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        # To fit into Admin, take arguments from parent 
        if kwargs.has_key('widget'):
            # Sometimes this is an instance, sometimes a class
            if hasattr(kwargs['widget'], 'attrs'):
                myattrs  = kwargs['widget'].attrs
            elif hasattr(kwargs['widget'](), 'attrs'):
                myattrs = kwargs['widget']().attrs

        kwargs.update({'widget' : TinyMCE(attrs=myattrs)})
        return super(HTMLField, self).formfield(**kwargs)