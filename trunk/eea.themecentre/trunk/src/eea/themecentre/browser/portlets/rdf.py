from Products.CMFPlone import utils
from Products.EEAContentTypes.interfaces import IFeedPortletInfo
from zope.component import getUtility

from eea.themecentre.themecentre import getTheme, getThemeTitle, getThemeCentre
from eea.themecentre.browser.portlets.catalog import BasePortlet
from eea.rdfrepository.interfaces import IRDFRepository
from eea.rdfrepository.utils import getRdfPortletData

class RDFPortlet(BasePortlet):

    def short_items(self):
        context = utils.context(self)
        currentThemeCentre = getThemeCentre(context)
        return getRdfPortletData(currentThemeCentre, max_items=3)

    def full_items(self):
        context = utils.context(self)
        feed_id = self.request['feed']

        currentTheme = getTheme(context)
        currentThemeTitle = getThemeTitle(context)
        search = { 'theme': currentTheme, 'theme_title': currentThemeTitle,
                   'id': feed_id }
        rdfrepository = getUtility(IRDFRepository)
        feeds = rdfrepository.getFeeds(search=search)

        if len(feeds) > 0:
            self.feedTitle = feeds[0].title
            feed = IFeedPortletInfo(feeds[0])
            return feed.items

        return []

    def title(self):
        return getattr(self, 'feedTitle', '')
