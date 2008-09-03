from django.contrib import admin

from django.contrib.contenttypes.models import ContentType

from django.db import models

from django.conf import settings

from base import Post

# This should be a relative import
from metaphore.admin import PostAdmin

def _pre_save(sender, instance, **kwargs):
    assert Post in instance._meta.parents, 'Trying to attach signal to something that\'s not a subclass of Post.'
    instance.content_type = ContentType.objects.get_for_model(instance.__class__)

def _register_type(sender, **kwargs):
    assert Post in sender._meta.parents, 'Trying to register something that\'s not a subclass of Post.'
    if settings.DEBUG:
        print 'Registering', sender
    
    # A workaround for Ticket #4470
    sender._meta.app_label = 'metaphore'

    admin.site.register(sender, PostAdmin)
    models.signals.pre_save.connect(_pre_save, sender=sender)
