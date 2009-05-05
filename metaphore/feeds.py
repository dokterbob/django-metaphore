from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from models import Post

class PostFeed(Feed):
    title = _('Post feed')
    description = _('Posts on the site.')
    
    def link(self):
        return reverse('metaphore-archive-index')
    
    def items(self):
        return Post.published_on_site.all()
        
    def item_author_name(self, item):
        return item.author_name()
    
    def item_pubdate(self, item):
        return item.publish_date

