from datetime import datetime

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.contrib.syndication.views import Feed

from basemodels import Post

class PostFeed(Feed):
    title = _('Post feed')
    description = _('Posts on the site.')
    
    def link(self):
        return reverse('metaphore-archive-index')
    
    def items(self):
        return Post.published_on_site.all()
        
    def item_author_name(self, item):
        return item.get_author_name()
    
    def item_pubdate(self, item):
        return datetime.combine(item.publish_date, item.publish_time)

    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.description