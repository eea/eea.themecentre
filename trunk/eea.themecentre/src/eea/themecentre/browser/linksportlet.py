from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from eea.themecentre.themecentre import getTheme

class EEALinksPortlet(utils.BrowserView):

    def published_link_items(self):
        context = utils.context(self)
        portal_catalog = getToolByName(context, 'portal_catalog')
        currentTheme = getTheme(context)
        result = []

        if currentTheme:
            query = { 'portal_type': 'Link',
                      'getThemes': currentTheme,
                      'sort_on': 'Date',
                      'sort_order': 'reverse',
                      'review_state': 'published' }

            for brain in portal_catalog(query):
                result.append({ 'title': brain.Title, 'url': brain.getURL() })

        return result
