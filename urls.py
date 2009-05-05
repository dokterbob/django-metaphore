from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

if settings.DEBUG:
    from os import path
    urlpatterns = patterns('django.views', (r'^static/(?P<path>.*)$', 'static.serve', {'document_root': path.join(settings.PROJECT_ROOT, 'static') }))
else:
    urlpatterns = patterns('')

from metaphore.feeds import PostFeed
feed_dict = {
    'posts' : PostFeed,
}

urlpatterns += patterns('',
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict':feed_dict}, name='feeds'),
)

urlpatterns += patterns('',
    # Django Admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^', include('metaphore.urls')),    
)
