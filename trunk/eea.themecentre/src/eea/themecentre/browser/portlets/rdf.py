from Products.CMFPlone import utils
from Products.EEAContentTypes.interfaces import IFeedPortletInfo
from Products.ThemeCentre.mergedtheme import getFeedsForSynonymousThemes
from zope.component import getUtility, getMultiAdapter
from zope.interface import implements

from eea.themecentre.themecentre import getTheme, getThemeTitle, getThemeCentre
from eea.themecentre.themecentre import RDF_THEME_KEY
from eea.themecentre.browser.interfaces import IRDFPortlet
from eea.themecentre.interfaces import IThemeCentrePortletInfo
from eea.themecentre.utils import localized_time
from eea.rdfrepository.interfaces import IRDFRepository

from eea.themecentre.browser.portlets.catalog import BasePortlet

class RDFPortlet(BasePortlet):

    def short_items(self):
        context = utils.context(self)
        currentTheme = getTheme(context)
        currentThemeCentre = getThemeCentre(context)

        if currentTheme:
            feeds = getFeedsForSynonymousThemes(currentTheme)

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
