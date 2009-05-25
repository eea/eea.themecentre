from eea.themecentre.themecentre import getTheme, getThemeCentre
from Products.CMFCore.utils import getToolByName
from eea.promotion.interfaces import IPromotion

class ThemeCentreMenuPromotion(object):
    """ Return the promotion to show as part of navigation. Most of the time an
        interactive map. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def promotions(self, section=None):
        currentTheme = getTheme(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        promotions = []

        # External promotions
        query = { 'portal_type' : 'Promotion',
                  'review_state' : 'published',
                  'getThemes' : currentTheme }
        if section is not None:
            query['navSection'] = section
        result = catalog.searchResults( query )
        for t in result:
            if (section is not None) or (section is None and t.navSection in [None, 'default']):
                promotions.append( {'id' : t.getId,
                                    'Description' : t.Description,
                                    'Title' : t.Title,
                                    'url' : t.getUrl,
                                    'style' : 'display: none;',
                                    'image' : t.getURL() + '/image' } )

        # Internal promotions
        query = {'object_provides': 'eea.promotion.interfaces.IPromoted',
                 'review_state': 'published'}
        result = catalog.searchResults(query)
        for t in result:
            promo = IPromotion(t.getObject())
            if not promo.display_on_themepage:
                continue
            if not currentTheme in promo.themes:
                continue
            if (section is not None) and (section != promo.themepage_section):
                continue
            if (section is not None) or (section is None and promo.themepage_section in [None, 'default']):
                promotions.append( {'id' : t.getId,
                                    'Description' : t.Description,
                                    'Title' : t.Title,
                                    'url' : t.getURL(),
                                    'style' : 'display: none;',
                                    'image' : t.getURL() + '/image' } )

        if promotions:
            promotions[0]['style'] = 'display: block'
        return promotions
