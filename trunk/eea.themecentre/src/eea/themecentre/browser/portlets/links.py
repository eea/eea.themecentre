from eea.themecentre.browser.portlets.catalog import CatalogBasePortlet
from Products.CMFPlone import utils

class LinksPortlet(CatalogBasePortlet):

    query = { 'portal_type': 'Link',
              'sort_on': 'Date',
              'sort_order': 'reverse',
              'review_state': 'published' }

    def all_link(self):
        context = utils.context(self)
        return context.absolute_url() + '/links'

    def item_to_short_dict(self, item):
        """ This method overrides the one in CatalogBasePortlet because
            the link's url should be the remote url, not the object's url. """

        return { 'title': item.Title,
                 'description': item.Description,
                 'url': item.getObject().getRemoteUrl(),
                 'detail': None }

    def item_to_full_dict(self, item):
        return { 'title': item.Title,
                 'description': item.Description,
                 'url': item.getObject().getRemoteUrl(),
                 'published': None }
