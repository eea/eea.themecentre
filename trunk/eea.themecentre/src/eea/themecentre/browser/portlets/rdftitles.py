from Products.CMFPlone import utils
from zope.component import getUtility

from eea.themecentre.themecentre import getTheme, getThemeTitle, getThemeCentre
from eea.themecentre.themecentre import RDF_THEME_KEY
from eea.rdfrepository.interfaces import IRDFRepository

from eea.themecentre.browser.portlets.catalog import BasePortlet

class RDFTitlesPortlet(BasePortlet):

    all_link = None
    
    def items(self):
        context = utils.context(self)
        currentTheme = getTheme(context)
        feeds = []

        if currentTheme:
            rdfrepository = getUtility(IRDFRepository)
            search = { RDF_THEME_KEY: { 'theme': currentTheme }}
            feeds = rdfrepository.getFeedData(search)
            
        return feeds

    def _feedListUrl(self, item):
        themeCentre = getThemeCentre(utils.context(self))
        return themeCentre.absolute_url() + \
               '/listfeed?feed=' + item['id']

    def item_to_short_dict(self, item):
        return  { 'title': item['title'],
                  'url': self._feedListUrl(item),
                  'detail': None }

    def item_to_full_dict(self, item):
        return  { 'title': item['title'],
                  'url': self._feedListUrl(item),
                  'description': '',
                  'body': '',
                  'published': None }

    def title(self):
        context = utils.context(self)
        return getThemeTitle(context)

    @property
    def size(self):
        return 10
