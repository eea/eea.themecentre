from Products.CMFPlone import utils
from Products.CMFCore.utils import getToolByName
from zope.component import queryAdapter
from zope.interface import implements
from eea.mediacentre.interfaces import IMultimedia
from eea.themecentre.browser.interfaces import IDocumentRelated
from p4a.video.interfaces import IMediaPlayer

class DocumentRelated(utils.BrowserView):
    implements(IDocumentRelated)

    def __init__(self, context, request):
        super(DocumentRelated, self).__init__(context, request)
        self.related = context.unrestrictedTraverse('computeRelatedItems')() or []

        self.related_feeds = []
        self.related_pages = []
        self.related_media = []
        self.related_other = []
        for item in self.related:
            if item.portal_type == 'RSSFeedRecipe':
                self.related_feeds.append(item)
            elif IMultimedia.providedBy(item):
                self.related_media.append(item)
            elif item.portal_type == 'Document':
                self.related_pages.append(item)
            else:
                self.related_other.append(item)

    def feeds(self):
        entries = []
        for item in self.related_feeds:
            feed = item.getFeed()
            for entry in feed:
                entries.append({ 'title': entry['title'],
                                 'url': entry['link'],
                                 'date': entry['updated_parsed'] })
        entries.sort(cmp=lambda x,y: cmp(x['date'], y['date']))
        return entries

    def multimedia(self):
        multimedia = []
        for item in self.related_media:
            mimetype = item.get_content_type()
            player_html = queryAdapter(item, name=mimetype, interface=IMediaPlayer)
            return player_html(None, None)
        return None

    def pages(self):
        pages = []
        for item in self.related_pages:
            pages.append({ 'title': item.Title(),
                           'url': item.absolute_url() })
        return pages

    def other(self):
        other = []
        context = utils.context(self)
        plone_utils = getToolByName(context, 'plone_utils')
        normalize = plone_utils.normalizeString

        portal_props = getToolByName(context, 'portal_properties')
        wf_tool = getToolByName(context, 'portal_workflow')
        site_props = portal_props.site_properties
        use_view = getattr(site_props, 'typesUseViewActionInListings', [])

        for item in self.related_other:
            item_type_class = normalize(item.portal_type)
            item_wf_state = wf_tool.getInfoFor(item, 'review_state', '')
            item_wf_state_class = 'state-' + normalize(item_wf_state)
            url = item.absolute_url()
            if item.portal_type in use_view:
                url += '/view'

            other.append({ 'title': item.Title(),
                           'description': item.Description(),
                           'url': url,
                           'item_type': item.portal_type,
                           'item_type_class': item_type_class,
                           'item_wf_state': item_wf_state,
                           'item_wf_state_class': item_wf_state_class })
        return other
