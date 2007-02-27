from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.portlets.news import NewsPortlet
from Products.CMFPlone import utils

from eea.themecentre.themecentre import getTheme

class EEANewsPortlet(NewsPortlet):

    def published_news_items(self):
        context = utils.context(self)
        portal_catalog = getToolByName(context, 'portal_catalog')
        currentTheme = getTheme(context)

        if currentTheme:
            query = { 'portal_type': 'News Item',
                      'getThemes': currentTheme,
                      'sort_on': 'Date',
                      'sort_order': 'reverse',
                      'review_state': 'published' }

            res = portal_catalog.searchResults(query)
        else:
            res = []

        return res
