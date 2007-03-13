from eea.themecentre.browser.portlets.catalog import CatalogBasePortlet

class NewsPortlet(CatalogBasePortlet):

    query = { 'portal_type': 'News Item',
              'sort_on': 'Date',
              'sort_order': 'reverse',
              'review_state': 'published' }

    def item_to_full_dict(self, item):
        return { 'title': item.Title,
                 'description': item.Description,
                 'url': item.getURL(),
                 'body': item.getObject().getText(),
                 'published': item.Date }
