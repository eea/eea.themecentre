from eea.themecentre.browser.portlets.catalog import CatalogBasePortlet

class FaqPortlet(CatalogBasePortlet):

    query = { 'portal_type': 'HelpCenterFAQ',
              'sort_on': 'Date',
              'sort_order': 'reverse',
              'review_state': 'published' }

    def item_to_full_dict(self, item):
        obj = item.getObject()

        return { 'title': item.Title,
                 'url': item.getURL(),
                 'body': '<p>' + item.Description + '</p>' + obj.getAnswer(),
                 'published': item.Date }
