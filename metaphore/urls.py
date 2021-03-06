from django.conf.urls.defaults import *

from metaphore.feeds import PostFeed

feed_urls = patterns('',
    url(r'^rss/$', PostFeed(), name='metaphore-feed-rss'),
)

blog_urls = patterns('metaphore.views',
   url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
         'metaphore_object_detail', name='metaphore-object-detail'),
   url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\w{1,2})/$',
         'metaphore_archive_day', name='metaphore-archive-day'),
   url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
         'metaphore_archive_month', name='metaphore-archive-month'),
   url(r'^(?P<year>\d{4})/$',
         'metaphore_archive_year', name='metaphore-archive-year'),
   url(r'^$',
         'metaphore_archive_index', name='metaphore-archive-index'),
)

urlpatterns = feed_urls + blog_urls
