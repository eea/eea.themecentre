from Products.CMFPlone import utils
from zope.interface import implements
from eea.mediacentre.interfaces import IMultimedia
from eea.themecentre.browser.interfaces import IDocumentRelated

class DocumentRelated(utils.BrowserView):
    implements(IDocumentRelated)

    def __init__(self, context, request):
        super(DocumentRelated, self).__init__(context, request)
        self.related = context.unrestrictedTraverse('computeRelatedItems')() or []

    def feeds(self):
        entries = []
        for item in self.related:
            if item.portal_type == 'RSSFeedRecipe':
                feed = item.getFeed()
                for entry in feed:
                    entries.append( { 'title': entry['title'],
                                      'url': entry['link'] } )
        entries.sort(cmp=lambda x,y: cmp(entry['updated_parsed'],
            entry['updated_parsed']))
        return entries

    def multimedia(self):
        multimedia = []
        for item in self.related:
            if IMultimedia.providedBy(item):
                multimedia.append(item.Title())
        return multimedia

    def pages(self):
        pages = []
        for item in self.related:
            if item.portal_type == 'Document':
                pages.append(item.Title())
        return pages
