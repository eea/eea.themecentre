from zope.component import queryAdapter
from eea.themecentre.themecentre import getThemeCentre
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from eea.themecentre.interfaces import IThemeTagging
from eea.themecentre.interfaces import IThemeCentreImageUrl
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

        catalog = getToolByName(context, 'portal_catalog')
        query = { 'object_provides' : 'eea.themecentre.interfaces.IThemeCentre',
                  'getId' : themeIds,
                  'review_state' : 'published' }
        result = catalog.searchResults(query)

        # return only the first 3 if more
        if len(result) > 3:
            result = result[:3]
        
        # arrange the themes in the order they are stored on the object
        themes_dict = {}
        themes_sorted = []
        language = self.request.get('LANGUAGE', 'en')
        for brain in result:
            theme = brain.getObject()
            translation = theme.getTranslation(language)
            if translation is not None:
                theme = translation
            themes_dict[theme.getId()] = theme
            
        for themeId in themeIds:
            theme = themes_dict.get(themeId, None)
            if theme:
                themes_sorted.append(theme)

        currentTheme = getThemeCentre(context)
        if currentTheme and currentTheme in themes_sorted:
            themes_sorted.remove(currentTheme)

        return themes_sorted

    def item_to_short_dict(self, item):
        res =  { 'title': item.Title(),
                 'url': item.absolute_url(),
                 'id': item.getId(),
                 'detail': None,
                 'image' : IThemeCentreImageUrl(item) }
        return res

    def item_to_full_dict(self, item):
        return { 'title': item.Title(),
                 'url': item.absolute_url(),
                 'id': item.getId(),
                 'published': None,
                 'image' : IThemeCentreImageUrl(item) }
