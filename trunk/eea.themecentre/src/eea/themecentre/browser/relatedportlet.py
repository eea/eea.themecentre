from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from eea.themecentre.themecentre import getThemeCentre
from eea.themecentre.interfaces import IThemeRelation

class EEARelatedPortlet(utils.BrowserView):

    def related(self):
        context = utils.context(self)
        portal_catalog = getToolByName(context, 'portal_catalog')
        reference_catalog = getToolByName(context, 'reference_catalog')
        currentThemeCentre = getThemeCentre(context)
        result = []

        if currentThemeCentre:
            relation = IThemeRelation(currentThemeCentre)
            for uid in relation.related:
                themeCentre = reference_catalog.lookupObject(uid)
                data = { 'title': themeCentre.Title(),
                         'url': themeCentre.absolute_url() }
                result.append(data)

        return result
