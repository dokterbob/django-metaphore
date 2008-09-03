from django.conf.urls.defaults import *

from django.views.generic.list_detail import object_list, object_detail

from models import *

list_dict = { 'queryset' : Post.published.all() }

urlpatterns = patterns('',
    (r'^$', object_list, list_dict),
    (r'^page(?P<page>[0-9]+)/$', object_list, list_dict),
    (r'^detail/(?P<object_id>[0-9]+)/$', object_detail, list_dict)
)
