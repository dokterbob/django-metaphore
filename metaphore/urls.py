from django.conf.urls.defaults import *

urlpatterns = patterns('',
   (r'(?P<content_type>\w+)/', include('metaphore.archive_urls'), ),
   (r'', include('metaphore.archive_urls')),    
)

