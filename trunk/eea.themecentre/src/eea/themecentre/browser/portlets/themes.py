from zope.component import queryAdapter
from eea.themecentre.themecentre import getThemeCentre
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from eea.themecentre.interfaces import IThemeTagging
from eea.themecentre.browser.portlets.catalog import BasePortlet

class ObjectThemesPortlet(BasePortlet):

    all_link = None

    def items(self):
        context = utils.context(self)
        adapter = queryAdapter(context, IThemeTagging, default=None)
        if adapter is None:
            return []

        themeIds = adapter.tags
        if themeIds == 'default':
            return []
        
        # return only the first 3 if more
        if len(themeIds) > 3:
            themeIds = themeIds[:3]

        catalog = getToolByName(context, 'portal_catalog')
        query = { 'object_provides' : 'eea.themecentre.interfaces.IThemeCentre',
                  'getId' : themeIds,
                  'review_state' : 'published' }
        result = catalog.searchResults(query)
        themes = [ brain.getObject() for brain in result ]

        currentTheme = getThemeCentre(context)
        if currentTheme and currentTheme in themes:
            themes.remove(currentTheme)

        return themes

    def item_to_short_dict(self, item):
        return { 'title': item.Title(),
                 'url': item.absolute_url(),
                 'id': item.getId(),
                 'detail': None }

    def item_to_full_dict(self, item):
        return { 'title': item.Title(),
                 'url': item.absolute_url(),
                 'id': item.getId(),
                 'published': None }
