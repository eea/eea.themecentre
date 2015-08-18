""" Related
"""
from Products.CMFCore.utils import getToolByName
from eea.themecentre.themecentre import getThemeCentre
from eea.themecentre.interfaces import IThemeRelation
from eea.themecentre.interfaces import IThemeCentreImageUrl
from eea.themecentre.browser.portlets.catalog import BasePortlet
from eea.themecentre import eeaMessageFactory as _


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
        current_theme_centre = getThemeCentre(context)
        result = []
        if current_theme_centre:
            catalog = getToolByName(context, 'portal_catalog')
            query = {
                'object_provides': 'eea.themecentre.interfaces.IThemeCentre',
                'review_state': 'published'}
            tcs = catalog.searchResults(query)
            tcs_ids = [brain.getId for brain in tcs]
            relation = IThemeRelation(current_theme_centre)
            language = self.request.get('LANGUAGE', 'en')
            for uid in relation.related:
                theme_centre = reference_catalog.lookupObject(uid)
                if theme_centre is not None and theme_centre.getId() in tcs_ids:
                    if theme_centre.hasTranslation(language):
                        theme_centre = theme_centre.getTranslation(language)
                    result.append(theme_centre)

        return result

    def item_to_short_dict(self, item):
        """ Item to short dict
        """
        return {'title': item.Title(),
                'url': item.absolute_url(),
                'detail': None,
                'image': IThemeCentreImageUrl(item)}

    def item_to_full_dict(self, item):
        """ Item to full dict
        """
        return {'title': item.Title(),
                'url': item.absolute_url(),
                'published': None,
                'image': IThemeCentreImageUrl(item)}
