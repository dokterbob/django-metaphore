import logging

from metaphore.models import Post


def latest_posts(request):
    return {'latest_posts': Post.published_on_site.all()}
