from datetime import datetime

from django.db.models import Manager
from django.contrib.sites.managers import CurrentSiteManager

class PublicationManager(Manager):
    def get_query_set(self):
        return super(Manager, self).get_query_set().filter(publish=True, publish_date__lte=datetime.now(), publish_time__lte=datetime.now())

class CurrentSitePublicationManager(CurrentSiteManager):
    def get_query_set(self):
        return super(CurrentSiteManager, self).get_query_set().filter(publish=True, publish_date__lte=datetime.now())
