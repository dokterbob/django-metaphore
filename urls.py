from django.conf.urls.defaults import *

from django.views.generic.list_detail import object_list

from models import *

list_dict = { 'paginate_by' : 4,
              'queryset' : Post.published()
            }

urlpatterns = patterns('',
    (r'^$', object_list, list_dict)
)
# (r'^$', object_list, {'page' : 1})
#  (r'^page(?P<page>[0-9]+)/$', object_list, list_dict)