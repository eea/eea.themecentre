from Products.CMFPlone import utils
from zope.component import getUtility
from zope.interface import implements

from eea.themecentre.themecentre import getTheme
from eea.themecentre.themecentre import RDF_THEME_KEY
from eea.themecentre.browser.interfaces import IRDFTitlesPortlet
from eea.rdfrepository.interfaces import IRDFRepository

class EEARDFTitlesPortlet(utils.BrowserView):
    implements(IRDFTitlesPortlet)

    def __init__(self, context, request):
        super(EEARDFTitlesPortlet, self).__init__(context, request)
        self._theme = getTheme(context)
        
    def feeds(self):
        context = utils.context(self)

        if self._theme:
            rdfrepository = getUtility(IRDFRepository)
            search = { RDF_THEME_KEY: { 'theme': self._theme }}
            return rdfrepository.getFeedData(search)

        return []

    def theme(self):
        return self._theme
