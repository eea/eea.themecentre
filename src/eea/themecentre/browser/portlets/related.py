""" Related
"""
from Products.CMFCore.utils import getToolByName
from eea.themecentre.themecentre import getThemeCentre
from eea.themecentre.interfaces import IThemeRelation
from eea.themecentre.interfaces import IThemeCentreImageUrl
from eea.themecentre.browser.portlets.catalog import BasePortlet
from eea.themecentre import _

class RelatedPortlet(BasePortlet):
    """ Related Portlet
    """

    all_link = None

    def title(self):
        """ Title
        """
        return _(u'Related themes')

    def items(self):
        """ Items
        """
        context = self.context
        reference_catalog = getToolByName(context, 'reference_catalog')
        currentThemeCentre = getThemeCentre(context)
        result = []
        if currentThemeCentre:
            catalog = getToolByName(context, 'portal_catalog')
            query = {
               'object_provides' : 'eea.themecentre.interfaces.IThemeCentre',
               'review_state' : 'published' }
            tcs = catalog.searchResults(query)
            tcsIds = [ brain.getId for brain in tcs ]
            relation = IThemeRelation(currentThemeCentre)
            language = self.request.get('LANGUAGE', 'en')
            for uid in relation.related:
                themeCentre = reference_catalog.lookupObject(uid)
                if themeCentre is not None and themeCentre.getId() in tcsIds:
                    if themeCentre.hasTranslation(language):
                        themeCentre = themeCentre.getTranslation(language)
                    result.append(themeCentre)

        return result

    def item_to_short_dict(self, item):
        """ Item to short dict
        """
        return { 'title': item.Title(),
                 'url': item.absolute_url(),
                 'detail': None,
                 'image' : IThemeCentreImageUrl(item) }

    def item_to_full_dict(self, item):
        """ Item to full dict
        """
        return { 'title': item.Title(),
                 'url': item.absolute_url(),
                 'published': None,
                 'image' : IThemeCentreImageUrl(item) }
