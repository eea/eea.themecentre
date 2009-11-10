from zope.component import getMultiAdapter
from eea.themecentre.themecentre import getTheme, getThemeCentre
from Products.CMFCore.utils import getToolByName
from eea.promotion.interfaces import IPromotion
from DateTime.DateTime import DateTime

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
        now = DateTime()

        result = catalog({
            'object_provides': {
                'query': [
                    'eea.promotion.interfaces.IPromoted',
                    'Products.EEAContentTypes.content.interfaces.IExternalPromotion',
                ],
                'operator': 'or',
            },
            'review_state': 'published',
            'effectiveRange' : now,
        })

        for brain in result:
            obj = brain.getObject()
            promo = IPromotion(obj)
            if not promo.display_on_themepage:
                continue
            if not currentTheme == promo.themes[0]:
                continue
            if (section is not None) and (section != promo.themepage_section):
                continue
            if (section is not None) or (section is None and promo.themepage_section in [None, 'default']):
                promotions.append({
                    'id' : brain.getId,
                    'Description' : brain.Description,
                    'Title' : brain.Title,
                    'url' : brain.getURL(),
                    'style' : 'display: none;',
                    'imglink' : getMultiAdapter((obj, obj.REQUEST),
                        name='promo_imglink')('thumb'),
                    'image' : brain.getURL() + '/image',
                })

        if promotions:
            promotions[0]['style'] = 'display: block'
        return promotions
