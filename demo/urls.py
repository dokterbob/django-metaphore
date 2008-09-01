from django.conf.urls.defaults import *

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    ('^admin/(.*)', admin.site.root),
    ('^stupid/(?P<id>\d+)/$', 'debugapp2.views.stupidformthingy')
    #(r'^', include('metablog.urls')),
)
