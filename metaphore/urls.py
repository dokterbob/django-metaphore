from copy import copy

from django.conf.urls.defaults import *
from django.conf import settings

from models import Post
base_dict = {
    'queryset': Post.published_on_site.all(),
    'date_field': 'publish_date',
}

index_dict = copy(base_dict)
index_dict.update({
    'template_object_name':'object_list'
})

year_dict = copy(base_dict)
year_dict.update({
    'make_object_list':True
})

month_dict = copy(base_dict)
month_dict.update({
    'month_format' : '%m'
})

urlpatterns = patterns('django.views.generic.date_based',
   url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', month_dict,  name='metaphore-object-detail'),
   url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\w{1,2})/$',                  'archive_day',   month_dict,  name='metaphore-archive-day'),
   url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',                                   'archive_month', month_dict,  name='metaphore-archive-month'),
   url(r'^(?P<year>\d{4})/$',                                                      'archive_year',  year_dict, name='metaphore-archive-year'),
   url(r'^$',                                                                      'archive_index', index_dict, name='metaphore-archive-index'),
)

