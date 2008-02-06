from Products.CMFCore.utils import getToolByName
from eea.themecentre.utils import localized_time
from eea.themecentre.themecentre import getThemeCentre
from zope.app.component.hooks import getSite
from DateTime import DateTime

DATE_FIELDS = ('start', 'end', 'EffectiveDate')

class SmartFolderPortlets(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        themecentre = getThemeCentre(self.context)
        if themecentre is None:
            return []

        catalog = getToolByName(getSite(), 'portal_catalog')
        query = { 'portal_type': 'Topic',
                  'path': '/'.join(themecentre.getPhysicalPath()) }
        brains = catalog.searchResults(query)
        portlets = []

        for brain in brains:
            topic = brain.getObject()
            extra_fields = topic.getCustomViewFields()

            portlet = {}
            portlet['entries'] = []
            portlet['title'] = self._title(topic)
            portlet['all_link'] = topic.aq_parent.absolute_url()
            portlet['sort_key'] = self._sort_key(topic)
            portlet['feed_link'] = topic.absolute_url() + '/RSS'

            topic_query = topic.buildQuery()
            topic_brains = catalog.searchResults(topic_query)[:3]
            for tb in topic_brains:
                item = { 'url': tb.getURL(),
                         'title': tb.Title,
                         'detail': self._detail(extra_fields, tb) }
                portlet['entries'].append(item)

            if portlet['entries']:
                portlets.append(portlet)

        portlets.sort(cmp=lambda x,y: cmp(x['sort_key'], y['sort_key']))

        return portlets

    def _detail(self, extra_fields, brain):
        detail = ''

        for index, field in enumerate(extra_fields):
            if field in DATE_FIELDS:
                if index > 0 and extra_fields[index-1] in DATE_FIELDS:
                    detail += ' - ' + localized_time(brain[field])
                else:
                    if detail:
                        detail += ', ' + localized_time(brain[field])
                    else:
                        detail += localized_time(brain[field])
            elif detail:
                detail += ', ' + brain[field]
            else:
                detail = brain[field]

        return detail

    def _sort_key(self, topic):
        id = topic.getId()

        if id == 'highlights_topic':
            return "1"
        elif id == 'events_topic':
            return "2"
        else:
            # all topics don't need to be hardcoded, for the rest we
            # rely on the topic id for sorting
            return id

    def _title(self, topic):
        parent = topic.aq_parent
        parent_id = parent.getId()
        parent_title = parent.Title()

        if parent_id == 'events':
            title = 'Upcoming events'
        elif parent_id == 'faq':
            title = 'Latest FAQ'
        else:
            title = 'Latest ' + parent_title.lower()
        return title
