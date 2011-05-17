""" RDF module
"""
from Products.CMFPlone import utils
from eea.themecentre.browser.portlets.catalog import BasePortlet
from eea.themecentre.themecentre import getTheme, getThemeTitle, getThemeCentre
from zExceptions import NotFound
from zope.component import getUtility
from eea.rdfrepository.interfaces import IRDFRepository
from eea.rdfrepository.utils import getRdfPortletData
#TODO: fix me, plone4
#from Products.EEAContentTypes.interfaces import IFeedPortletInfo
#TODO: fix me, plone4
# - just delete the dummy interface
from zope.interface import Interface
class IFeedPortletInfo(Interface):
    """ Dummy interface
    """

class RDFPortlet(BasePortlet):
    """ RDF Portlet
    """

    def short_items(self):
        """ Short items
        """
        context = utils.context(self)
        currentThemeCentre = getThemeCentre(context)
        return getRdfPortletData(currentThemeCentre, max_items=3)

    def full_items(self):
        """ Full items
        """
        feed_id = self.request.get('feed')
        if not feed_id:
            raise NotFound

        context = utils.context(self)
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
        """ Title
        """
        return getattr(self, 'feedTitle', '')
