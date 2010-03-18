from django.conf.urls.defaults import *

urlpatterns = patterns('metaphore.views',
   (r'(?P<content_type>\w+)/', include('metaphore.post_urls'), ),
   (r'', include('metaphore.post_urls')),    
)

