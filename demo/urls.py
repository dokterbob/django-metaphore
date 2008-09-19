from django.conf.urls.defaults import *

from django.contrib import admin

admin.autodiscover()

from django.conf import settings

if settings.DEBUG:
    from os import path
    urlpatterns = patterns('django.views', (r'^static/(?P<path>.*)$', 'static.serve', {'document_root': path.join(settings.PROJECT_ROOT, 'static') }))
else:
    urlpatterns = patterns('')

urlpatterns += patterns('',
    # Django admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    ('^admin/(.*)', admin.site.root),
    
    # Metaphore
    (r'^', include('metaphore.urls')),
)
