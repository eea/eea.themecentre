from zope.component import queryMultiAdapter
from eea.themecentre.browser.portlets.catalog import BasePortlet

class FacetedPortlet(BasePortlet):

    @property
    def all_link(self):
        context = self.context[0]
        return context.absolute_url()

    @property
    def title(self):
        context = self.context[0]
        return context.Title()
    
    def items(self):
        context = self.context[0]
        facetednav = queryMultiAdapter((context, self.request), name=u'faceted_query')
        query = facetednav.default_criteria
        return facetednav.query(batch=False, sort=True, **query)

    def __call__(self):
        context = self.context[0]
        items = self.items()[:self.size]
        if items:
            return {
                'title': self.title,
                'all_link': self.all_link,
                'entries': [self.item_to_short_dict(item) for item in items],
                'feed_link': context.absolute_url() + '/RSS',
            }

    def item_to_short_dict(self, item):
        return {
            'title': item.Title,
            'url': item.getURL(),
            'id': item.id,
            'detail': None,
            'Image': item.getURL() + '/image_thumb',
         }

    def item_to_full_dict(self, item):
        return {
            'title': item.Title,
            'url': item.getURL(),
            'id': item.id,
            'published': None,
            'Image': item.getURL() + '/image_thumb',
        }
