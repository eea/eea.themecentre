from zope.interface import implements, alsoProvides
from zope.component import getUtility
from zope.event import notify
from zope.formlib.form import Fields, EditForm
from eea.themecentre.interfaces import IThemeCentre, IPossibleThemeCentre
from eea.themecentre.interfaces import IThemeCentreSchema
from eea.themecentre.themecentre import PromotedToThemeCentreEvent
from Products.CMFCore.utils import getToolByName

from eea.mediacentre.interfaces import IMediaCentre

ENABLE = 1 # Manual mode from ATContentTypes.lib.constraintypes

class PromoteThemeCentre(object):
    """ Promote a folder to a theme centre. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        alsoProvides(self.context, IThemeCentre)
        types = [ 'Folder', 'Document', 'Link', 'File', 'Image', 'Event','FlashFile' ]
        
        self.context.setLocallyAllowedTypes( types + ['RichTopic', 'Topic'] )
        self.context.setImmediatelyAddableTypes( types )
        self.context.setConstrainTypesMode(ENABLE)
        self.context.layout = 'themecentre_view'
        notify(PromotedToThemeCentreEvent(self.context))
        return self.request.RESPONSE.redirect(self.context.absolute_url() + '/themecentre_edit.html')
    
class ThemeCentreEdit(EditForm):
    """ Form for setting theme for a theme centre. """

    form_fields = Fields(IThemeCentreSchema)
    label = u'Promote theme centre'


class ThemeCentre(object):
    implements(IThemeCentre)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.theme = IThemeCentreSchema(context).tags
        self.catalog = getToolByName(context, 'portal_catalog')
        self.mediacentre = getUtility(IMediaCentre)

    def _getRSS(self, query):
        feeds = self.catalog.searchResults( query )
        filterUrl = []
        result = []
        for feed in feeds:
            feed = feed.getObject()
            for item in feed.getFeed():
                if item.getURL() not in filterUrl:
                    result.append(item)
                    filterUrl.append(item.getURL())
        return result
    
    def getReports(self):
        query = { 'portal_type' : 'RSSFeedRecipe',
                  'path' : '/'.join(self.context.getPhysicalPath()),
                  'Title' : 'Reports' }
        result = self.catalog.searchResults( query )
        if len(result) > 0:
            return result[0].getObject()
        return None
    
    def getHighlights(self):
        query = { 'portal_type' : 'Highlight',
                  'getThemes' : self.theme }
        return self.catalog.searchResults( query )

    def getArticles(self):
        """ return a list of articles for this theme centre. """

    def getIndicators(self):
        """ return a list of indicators for this theme centre. """

    def getData(self):
        """ return a list of data from data service for this theme centre. """

    def getLinks(self):
        query = { 'portal_type' : 'Link',
                  'path' : '/'.join(self.context.getPhysicalPath()) }
        return self.catalog.searchResults( query )
        
    def getVideos(self):
        query = { 'portal_type' : 'FlashFile',
                  'getThemes' : self.theme }
        return self.catalog.searchResults( query )

