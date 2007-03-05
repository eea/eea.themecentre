from Products.CMFPlone import utils
from zope.component import getUtility
from zope.interface import implements

from eea.themecentre.themecentre import getTheme
from eea.themecentre.themecentre import RDF_THEME_KEY
from eea.themecentre.browser.interfaces import IRDFPortlet
from eea.rdfrepository.interfaces import IRDFRepository

class EEARDFPortlet(utils.BrowserView):
    implements(IRDFPortlet)

    def feeds(self):
        context = utils.context(self)
        currentTheme = getTheme(context)

        result = []

        if currentTheme:
            rdfrepository = getUtility(IRDFRepository)
            search = { RDF_THEME_KEY: { 'theme': currentTheme }}
            feed = rdfrepository.getFeedData(search)

            for struct in feed:
                data = { 'title': struct['title'],
                         'url': struct['link'] }
                result.append(data)

        return result
