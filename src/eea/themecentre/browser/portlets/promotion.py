""" Promotion
"""
from zope.interface import Interface
from zope.component import queryAdapter
from Products.CMFCore.utils import getToolByName
from DateTime.DateTime import DateTime
try:
    from eea.promotion.interfaces import IPromotion
except ImportError:
    class IPromotion(Interface):
        """ IPromotion """

try:
    from eea.mediacentre.interfaces import IVideo
except ImportError:
    class IVideo(Interface):
        """ IVideo """
from eea.themecentre.themecentre import getTheme


class ThemeCentreMenuPromotion(object):
    """ Return the promotion to show as part of navigation. Most of the time an
        interactive map.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def promotions(self, section=None):
        """ Promotions
        """
        currentTheme = getTheme(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        promotions = []
        now = DateTime()

        result = catalog({
            'object_provides': {
                'query': [
          'eea.promotion.interfaces.IPromoted',
          'Products.EEAContentTypes.content.interfaces.IExternalPromotion', ],
                'operator': 'or',
            },
            'review_state': 'published',
            'effectiveRange' : now,
        })

        for brain in result:
            obj = brain.getObject()
            promo = queryAdapter(obj, IPromotion)
            if not promo:
                continue
            if not promo.display_on_themepage:
                continue
            if not promo.themes or not currentTheme == promo.themes[0]:
                continue
            if (section is not None) and (section != promo.themepage_section):
                continue
            if (section is not None) or \
                           (section is None and \
                            promo.themepage_section in [None, 'default']):
                uid = brain.getId
                ids = [i['id'] for i in promotions]
                count = 0
                while uid in ids:
                    count += 1
                    new_id = uid + '-' + str(count)
                    if not new_id in ids:
                        uid = new_id
                promotions.append({
                    'id' : uid,
                    'Description' : brain.Description,
                    'Title' : brain.Title,
                    'url' : promo.url,
                    'absolute_url' : brain.getURL(),
                    'is_video' : IVideo.providedBy(obj),
                })

        return promotions
