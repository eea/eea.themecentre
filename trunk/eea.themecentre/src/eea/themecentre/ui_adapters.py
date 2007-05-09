from zope.component import adapts
from zope.interface import implements
from eea.themecentre.interfaces import IThemeCentrePortletInfo
from eea.themecentre.interfaces import IThemeCentrePortletItem
from eea.themecentre.interfaces import IThemeCentre
from eea.themecentre.interfaces import IThemeCentreListFeed
from eea.rdfrepository.interfaces import IFeedInfo, IFeedItem
from eea.themecentre.utils import localized_time

class FeedPortletInfo(object):
    implements(IThemeCentrePortletInfo)
    adapts(IThemeCentre, IFeedInfo)
    
    def __init__(self, themecentre, feed):
        self.themecentre = themecentre
        self.feed = feed

    @property
    def id(self):
        return self.feed.id

    @property
    def title(self):
        return self.feed.title

    @property
    def url(self):
        return self.feed.url

    @property
    def more_link(self):
        return self.themecentre.absolute_url() + '/listfeed?feed=' + self.feed.id

    @property
    def items(self):
        return [IThemeCentrePortletItem(item) for item in self.feed.items]


class FeedItemPortletInfo(object):
    implements(IThemeCentrePortletItem)
    adapts(IFeedItem)

    def __init__(self, item):
        self.item = item

    @property
    def title(self):
        return self.item.title

    @property
    def url(self):
        return self.item.url

    @property
    def detail(self):
        published = self.item.get('published')
        if published:
            return localized_time(published)
        else:
            return None

    @property
    def image(self):
        return self.item.get('image')


class ListFeedInfo(object):
    implements(IThemeCentreListFeed)
    adapts(IFeedItem)

    def __init__(self, item):
        self.item = item

    @property
    def title(self):
        return self.item.title

    @property
    def url(self):
        return self.item.url

    @property
    def summary(self):
        return self.item.get('summary')

    @property
    def published(self):
        published = self.item.get('published')
        if published:
            return localized_time(published)
        else:
            return None
