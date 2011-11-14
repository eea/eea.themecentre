from Products.CMFPlone import utils
from zope.component import getUtility

from eea.themecentre.themecentre import getTheme, getThemeTitle, getThemeCentre
from eea.rdfrepository.interfaces import IRDFRepository

from eea.themecentre.browser.portlets.catalog import BasePortlet

class RDFTitlesPortlet(BasePortlet):

    all_link = None
    
    def __call__(self):
        items = self.items()

        portlet = {}
        portlet['title'] = 'EEA products'
        portlet['all_link'] = None
        portlet['entries'] = []
        portlet['feed_link'] = None

        for item in items[:self.size]:
            entry = self.item_to_short_dict(item)
            portlet['entries'].append(entry)

        if portlet['entries']:
            return portlet
        else:
            return None

    def items(self):
        context = utils.context(self)
        currentTheme = getTheme(context)
        currentThemeTitle = getThemeTitle(context)
        feeds = []

        if currentTheme:
            rdfrepository = getUtility(IRDFRepository)
            search = { 'theme': currentTheme,
                       'theme_title': currentThemeTitle }
            feeds = rdfrepository.getFeeds(search=search)
            
        return feeds

    def _feedListUrl(self, item):
        themeCentre = getThemeCentre(utils.context(self))
        return themeCentre.absolute_url() + \
               '/listfeed?feed=' + item.id

    def item_to_short_dict(self, item):
        return  { 'title': item.title,
                  'url': self._feedListUrl(item),
                  'detail': None }

    def item_to_full_dict(self, item):
        return  { 'title': item.title,
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
