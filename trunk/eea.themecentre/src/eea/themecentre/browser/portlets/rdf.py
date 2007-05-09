from Products.CMFPlone import utils
from zope.component import getUtility, getMultiAdapter
from zope.interface import implements

from eea.themecentre.themecentre import getTheme, getThemeCentre
from eea.themecentre.themecentre import RDF_THEME_KEY
from eea.themecentre.browser.interfaces import IRDFPortlet
from eea.themecentre.interfaces import IThemeCentrePortletInfo
from eea.themecentre.interfaces import IThemeCentreListFeed
from eea.themecentre.utils import localized_time
from eea.rdfrepository.interfaces import IRDFRepository

from eea.themecentre.browser.portlets.catalog import BasePortlet

class RDFPortlet(BasePortlet):

    def short_items(self):
        context = utils.context(self)
        currentTheme = getTheme(context)
        currentThemeCentre = getThemeCentre(context)

        if currentTheme:
            rdfrepository = getUtility(IRDFRepository)
            search = { 'theme': currentTheme }
            feeds = [feed for feed in rdfrepository.getFeeds(search=search)
                     if feed.id not in ('Atlas', 'datasets')]

            for feed in feeds:
                feed.items = feed.items[:self.size]

            return [getMultiAdapter((currentThemeCentre, feed),
                                     IThemeCentrePortletInfo)
                    for feed in feeds]
        else:
            return []

    def full_items(self):
        context = utils.context(self)
        feed_id = self.request['feed']
        result = []

        currentTheme = getTheme(context)
        search = { 'theme': currentTheme, 'id': feed_id }
        rdfrepository = getUtility(IRDFRepository)
        feeds = rdfrepository.getFeeds(search=search)

        if len(feeds) > 0:
            self.feedTitle = feeds[0].title
            for item in feeds[0].items:
                item = IThemeCentreListFeed(item)
                result.append(item)

        return result

    def title(self):
        return getattr(self, 'feedTitle', '')
