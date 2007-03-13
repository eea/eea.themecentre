from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from eea.themecentre.browser.portlets.catalog import CatalogBasePortlet

class EventsPortlet(CatalogBasePortlet):

    query = { 'portal_type': 'Event',
              'end': { 'query': DateTime(), 'range': 'min' },
              'sort_on': 'start',
              'sort_limit': 5,
              'review_state': 'published' }

    def item_to_short_dict(self, item):
        return { 'title': item.Title,
                 'description': item.Description,
                 'url': item.getURL(),
                 'detail': self.localized_time(item.start) }

    def item_to_full_dict(self, item):
        return { 'title': item.Title,
                 'description': item.location,
                 'url': item.getURL(),
                 'body': item.Description,
                 'published': self.localized_time(item.start) }
