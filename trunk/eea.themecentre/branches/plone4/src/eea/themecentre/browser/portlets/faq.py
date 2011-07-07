""" FAQ
"""
from eea.themecentre.browser.portlets.catalog import CatalogBasePortlet

from Products.CMFCore.utils import getToolByName

class FaqPortlet(CatalogBasePortlet):
    """ Faq Portlet
    """

    query = { 'portal_type': 'HelpCenterFAQ',
              'sort_on': 'Date',
              'sort_order': 'reverse',
              'review_state': 'published' }

    def item_to_short_dict(self, item):
        """ Item to short dict
        """
        return {
            'title': item.Title,
            'url': item.getURL(),
         }

    def item_to_full_dict(self, item):
        """ Item to full dict
        """
        obj = item.getObject()
        return { 'title': item.Title,
                 'url': item.getURL(),
                 'detail': item.Description + obj.getText(),
                 'Image': None,
                 'published': item.Date }

    def items(self):
        """ Items
        """
        context = self.context
        portal_catalog = getToolByName(context, 'portal_catalog')
        res = portal_catalog.searchResults(self.query)
        return res


    #NOTE: plone4 this is here if you want to change the template from 
    # simple-list macro to portlet from portlet_themes_common to get the 
    # detail of the faq as well, not just the url and title

    def __call__(self):
        context = self.context
        items = self.items()[:self.size]
        if items:
            return {
               'title': self.context.title,
               'all_link': None,
               'entries': [self.item_to_full_dict(item) for item in items],
               'short_items': [self.item_to_short_dict(item) for item in items],
               'feed_link': context.absolute_url() + '/RSS',
            }
