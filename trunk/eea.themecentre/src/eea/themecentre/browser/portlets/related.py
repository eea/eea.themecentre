from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from eea.themecentre.themecentre import getThemeCentre
from eea.themecentre.interfaces import IThemeRelation
from eea.themecentre.browser.portlets.catalog import BasePortlet

class RelatedPortlet(BasePortlet):

    all_link = None

    def items(self):
        context = utils.context(self)
        reference_catalog = getToolByName(context, 'reference_catalog')
        currentThemeCentre = getThemeCentre(context)
        result = []
        if currentThemeCentre:
            relation = IThemeRelation(currentThemeCentre)
            for uid in relation.related:
                themeCentre = reference_catalog.lookupObject(uid)
                if themeCentre is not None:
                    result.append(themeCentre)

        return result

    def item_to_short_dict(self, item):
        return { 'title': item.Title(),
                 'url': item.absolute_url(),
                 'detail': None }

    def item_to_full_dict(self, item):
        return { 'title': item.Title(),
                 'url': item.absolute_url(),
                 'published': None }
