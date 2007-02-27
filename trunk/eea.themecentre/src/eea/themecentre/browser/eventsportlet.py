from Products.CMFPlone.browser.portlets.events import EventsPortlet
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from DateTime import DateTime

from eea.themecentre.themecentre import getTheme

class EEAEventsPortlet(EventsPortlet):

    def published_events(self):
        context = utils.context(self)
        portal_catalog = getToolByName(context, 'portal_catalog')
        currentTheme = getTheme(context)

        query = { 'portal_type': 'Event',
                  'end': { 'query': DateTime(), 'range': 'min' },
                  'sort_on': 'start',
                  'sort_limit': 5,
                  'review_state': 'published',
                  'getThemes': currentTheme }

        return portal_catalog.searchResults(query)[:5]
