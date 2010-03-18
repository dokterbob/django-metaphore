from django.conf.urls.defaults import *

urlpatterns = patterns('metaphore.views',
   (r'', include('metaphore.post_urls')),    
   
   (r'(?P<content_type>\w{1})/', include('metaphore.post_urls'),)
)

