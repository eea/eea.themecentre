from eea.themecentre.browser.portlets.catalog import CatalogBasePortlet
from Products.CMFPlone import utils
from DateTime import DateTime

class HighlightsPortlet(CatalogBasePortlet):

    def __init__(self, context, request):
        super(HighlightsPortlet, self).__init__(context, request)
        self.query = {
            'portal_type': ( 'Highlight', 'News Item' ),
            'sort_on': 'effective',
            'sort_order': 'reverse',
            'review_state': 'published',
            'effectiveRange' : DateTime() }

    def all_link(self):
        context = utils.context(self)
        return context.absolute_url() + '/highlights'

    def item_to_full_dict(self, item):
        return { 'title': item.Title,
                 'description': item.Description,
                 'url': item.getURL(),
                 'body': item.getObject().getText(),
                 'published': item.Date }
