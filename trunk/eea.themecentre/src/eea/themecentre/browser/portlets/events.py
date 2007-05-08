from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from eea.themecentre.browser.portlets.catalog import CatalogBasePortlet

class EventsPortlet(CatalogBasePortlet):

    def __init__(self, context, request):
        super(EventsPortlet, self).__init__(context, request)
        self.query = {
            'portal_type': ( 'Event', 'QuickEvent', 'RDFEvent' ),
            'end': { 'query': DateTime(), 'range': 'min' },
            'sort_on': 'start',
            'sort_limit': 5,
            'review_state': 'published' }

    def all_link(self):
        context = utils.context(self)
        return context.absolute_url() + '/events'

    def item_to_short_dict(self, item):
        detail = self.localized_time(item.start) + " - " + \
                 self.localized_time(item.end)
        if item.location:
            detail += ", " + item.location

        return { 'title': item.Title,
                 'description': item.Description,
                 'url': item.getURL(),
                 'detail': detail }

    def item_to_full_dict(self, item):
        return { 'title': item.Title,
                 'description': item.location,
                 'url': item.getURL(),
                 'body': item.Description,
                 'published': self.localized_time(item.start) }
