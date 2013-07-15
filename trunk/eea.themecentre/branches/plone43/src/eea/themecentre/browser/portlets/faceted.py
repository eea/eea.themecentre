""" Faceted
"""
from zope.component import queryMultiAdapter
from eea.themecentre.browser.portlets.catalog import BasePortlet
from types import GeneratorType
import itertools
import logging

log = logging.getLogger("eea.themecentre")

class FacetedPortlet(BasePortlet):
    """ Faceted Portlet
    """

    @property
    def all_link(self):
        """ All link
        """
        context = self.context
        return context.absolute_url()

    @property
    def title(self):
        """ Title
        """
        context = self.context
        return context.Title()

    def items(self):
        """ Items
        """
        context = self.context
        facetednav = queryMultiAdapter((context, self.request),
                                       name=u'faceted_query')
        if facetednav is None:
            logging.warn("faceted_query view could not be found for %s, "
                         "returning nothing." % context)
            return []
        query = facetednav.default_criteria
        return facetednav.query(batch=False, sort=True, **query)

    def __call__(self):
        context = self.context
        items = self.items()
        # NOTE: plone4 items is now a generator if found else an empty batch
        if isinstance(items, GeneratorType):
            items = list(itertools.islice(items, self.size))
        else:
            items = None
        if items:
            return {
                'title': self.title,
                'all_link': self.all_link,
                'entries': [self.item_to_short_dict(item) for item in items],
                'feed_link': context.absolute_url() + '/RSS',
            }

    def item_to_short_dict(self, item):
        """ Item to short dict
        """
        return {
            'title': item.Title,
            'url': item.getURL(),
            'id': item.id,
            'detail': None,
            'Image': item.getURL() + '/image_thumb',
         }

    def item_to_full_dict(self, item):
        """ Item to full dict
        """
        return {
            'title': item.Title,
            'url': item.getURL(),
            'id': item.id,
            'published': None,
            'Image': item.getURL() + '/image_thumb',
        }
