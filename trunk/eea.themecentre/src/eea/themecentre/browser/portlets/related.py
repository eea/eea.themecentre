from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from eea.themecentre.themecentre import getThemeCentre
from eea.themecentre.interfaces import IThemeRelation
from eea.themecentre.browser.portlets.catalog import BasePortlet

class RelatedPortlet(BasePortlet):

    def items(self):
        context = utils.context(self)
        reference_catalog = getToolByName(context, 'reference_catalog')
        currentThemeCentre = getThemeCentre(context)
        result = []

        if currentThemeCentre:
            relation = IThemeRelation(currentThemeCentre)
            for uid in relation.related:
                themeCentre = reference_catalog.lookupObject(uid)
                result.append(themeCentre)

        return result

    def item_to_short_dict(self, item):
        return { 'title': item.Title(),
                 'url': item.absolute_url(),
                 'detail': self.localized_time(item.modified()) }

    def item_to_full_dict(self, item):
        return { 'title': item.Title(),
                 'url': item.absolute_url(),
                 'published': self.localized_time(item.modified()) }
