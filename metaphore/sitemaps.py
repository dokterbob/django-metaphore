from django.contrib.sitemaps import Sitemap
from basemodels import Post

class PostSitemap(Sitemap):
    def lastmod(self, item):
        return item.modify_date
    
    def items(self):
        return Post.published_on_site.all()
