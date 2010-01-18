from Products.CMFCore.utils import getToolByName
from eea.themecentre.themecentre import getThemeCentre

def uids(context):
    catalog = getToolByName(context, 'portal_catalog')
    query = { 'path': '/'.join(context.getPhysicalPath()) }
    uids = [ brain.portal_linkchecker_uid
             for brain in catalog.searchResults(query) ]
    return uids

class ThemeCentreLinkChecker(object):
    """ Provides links for the content manager to investigate. """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self._result = {}

        self._generate_data()

        self._result['states'] = [
            ('red', 'Red'),
            ('orange', 'Orange'),
            ('green', 'Green'),
            ('grey', 'Grey'),
        ]

        return self._result

    def redirect(self):
        self.request.RESPONSE.redirect('../linkchecker_summary')

    def showInTab(self):
        themecentre = getThemeCentre(self.context)
        if not themecentre:
            return False

        context_uid = self.context.UID()
        check_for = [themecentre.UID()]

        default_page = getattr(themecentre, 'default_page', None)
        if default_page:
            default_object = getattr(themecentre, default_page, None)
            if default_object:
                check_for += [default_object.UID()]

        if context_uid in check_for:
            return True
        else:
            return False

    def _generate_data(self):
        lc = getToolByName(self.context, 'portal_linkchecker')
   
        themecentre = getThemeCentre(self.context)
        links = lc.database.query(objects=uids(themecentre))

        document_counts = []
        link_count_per_document = {}
        link_count_per_state = {'red': 0, 'grey': 0, 'green': 0, 'orange': 0}
        documents_per_state = {'red': {}, 'grey': {}, 'green': {}, 'orange': {}}

        for link in links:
            document_counts.append(len(link.objects))
            link_count_per_state[link.state] += 1

            documents = documents_per_state[link.state]
            for uid in link.objects:
                count = link_count_per_document.get(uid, 0)
                link_count_per_document[uid] = count + 1
                documents[uid] = True

        # totals
        self._result['totalDistinctLinks'] = len(links)
        self._result['totalLinks'] = sum(document_counts)
        self._result['totalDocuments'] = len(link_count_per_document)

        # links in state
        self._result['links'] = link_count_per_state
        if links:
            self._result['linksPct'] = {}
            for state, count in link_count_per_state.items():
                self._result['linksPct'][state] = float(count) / \
                         self._result['totalDistinctLinks'] * 100
        else:
            self._result['linksPct'] = link_count_per_state

        # documents in state
        self._result['documents'] = {}
        self._result['documentsPct'] = {}
        if self._result['totalDocuments']:
            for state, docs in documents_per_state.items():
                count = len(docs)
                self._result['documents'][state] = count
                self._result['documentsPct'][state] = float(count) / \
                        self._result['totalDocuments'] * 100

class LinksByStatus(object):
    """ Retrieves all documents that have broken links. """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.state = self.request.get('link_state')
        self.lc = getToolByName(self.context, 'portal_linkchecker')

    def documents(self):
        documents = {}

        for link, doc, member in self._document_iterator():
            key = doc.getURL()
            item = documents.get(key)
            if item is None:
                item = documents[key] = {}
                item['document'] = doc
                item['total'] = self._total_links(doc)
                item['instate'] = 0
                if member is None:
                    item["owner_mail"] = ""
                    item["owner"] = doc.Creator
                else:
                    item["owner_mail"] = member.getProperty("email")
                    item["owner"] = member.getProperty("fullname", doc.Creator)
            
            item["instate"] += 1
        
        return documents.values()
        
    def links(self):
        """Returns a list of links in the given state."""

        items = []

        for link, doc, member in self._document_iterator():
            item = {}
            item["url"] = link.url
            item["reason"] = link.reason
            item["lastcheck"] = link.lastcheck
            item["document"] = doc
            
            if member is None:
                item["owner_mail"] = ""
                item["owner"] = doc.Creator
            else:
                item["owner_mail"] = member.getProperty("email")
                item["owner"] = member.getProperty("fullname", doc.Creator)
                
            items.append(item)

        return items

    def _document_iterator(self):
        member_cache = {}
        catalog = getToolByName(self, 'portal_catalog')
        pms = getToolByName(self, 'portal_membership')

        _marker = object()

        themecentre = getThemeCentre(self.context)
        links = self.lc.database.query(state=[self.state],
                                       objects=uids(themecentre))
        for link in links:
            doc_uids = link.objects
            if not doc_uids:
               continue
            docs = catalog(portal_linkchecker_uid=doc_uids, Language='all')
            for doc in docs:
                creator = doc.Creator
                member = member_cache.get(creator, _marker)
                if member is _marker:
                    member = pms.getMemberById(creator)
                    member_cache[creator] = member
                yield link, doc, member

    def _total_links(self, doc):
        uid = self.lc.getUIDForBrain(doc)
        links = self.lc.database.query(objects=[uid])
        return
