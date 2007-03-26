from Products.CMFPlone import utils
from zope.component import getUtility

from eea.themecentre.themecentre import getTheme, getThemeTitle
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

    def item_to_short_dict(self, item):
        return  { 'title': item['title'],
                  'url': item['url'],
                  'detail': None }

    def item_to_full_dict(self, item):
        return  { 'title': item['title'],
                  'url': item['url'],
                  'description': '',
                  'body': '',
                  'published': None }

    def title(self):
        context = utils.context(self)
        return getThemeTitle(context)
