from eea.themecentre.themecentre import getTheme, getThemeCentre
from Products.CMFCore.utils import getToolByName

class ThemeCentreMenuPromotion(object):
    """ Return the promotion to show as part of navigation. Most of the time an
        interactive map. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        currentTheme = getTheme(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        result = catalog.searchResults( { 'portal_type' : 'Promotion',
                                          'review_state' : 'published',
                                          'getThemes' : currentTheme } )
        promotions = []

        for t in result:
                promotions.append( {'id' : t.getId,
                                    'Description' : t.Description,
                                    'Title' : t.Title,
                                    'url' : t.getUrl,
                                    'style' : 'display: block;',
                                    'image' : t.getURL() + '/image' } )
        return promotions
