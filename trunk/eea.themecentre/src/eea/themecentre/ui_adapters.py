from zope.component import adapts
from zope.interface import implements
from eea.themecentre.interfaces import IThemeCentrePortletInfo
from eea.themecentre.interfaces import IThemeCentrePortletItem
from eea.themecentre.interfaces import IThemeCentre
from eea.themecentre.interfaces import IThemeCentreListFeed
from eea.rdfrepository.interfaces import IFeedInfo, IFeedItem, IFeed
from eea.themecentre.utils import localized_time
from Products.CMFCore.utils import getToolByName
from Products.EEAContentTypes import feeds

class FeedPortletInfo(feeds.FeedPortletInfo):
    implements(IThemeCentrePortletInfo)
    adapts(IThemeCentre, IFeed)
    
    def __init__(self, themecentre, feed):
        self.themecentre = themecentre
        self.feed = feed

    @property
    def more_link(self):
        tc = self.themecentre
        catalog = getToolByName(tc, 'portal_catalog')
        res = catalog.searchResults(path='/'.join(tc.getPhysicalPath()),
                                    depth=1,
                                    Title=self.feed.title)
        if len(res) == 1:
            return res[0].getURL()
        return self.themecentre.absolute_url() + '/listfeed?feed=' + self.feed.id


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

