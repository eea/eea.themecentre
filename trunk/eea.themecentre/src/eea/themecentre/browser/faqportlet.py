from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from eea.themecentre.themecentre import getTheme

class EEAFaqPortlet(utils.BrowserView):

    def published_faq_items(self):
        context = utils.context(self)
        portal_catalog = getToolByName(context, 'portal_catalog')
        currentTheme = getTheme(context)
        result = []

        if currentTheme:
            query = { 'portal_type': 'HelpCenterFAQ',
                      'getThemes': currentTheme,
                      'sort_on': 'Date',
                      'sort_order': 'reverse',
                      'review_state': 'published' }

            for brain in portal_catalog.searchResults(query):
                result.append({ 'title': brain.Title, 'url': brain.getURL() })

        return result
