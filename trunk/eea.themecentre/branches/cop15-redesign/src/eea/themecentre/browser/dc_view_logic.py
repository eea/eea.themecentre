from zope.component import queryMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from eea.rdfrepository.interfaces import IFeed
from eea.themecentre.themecentre import getThemeCentre
from Products.NavigationManager.sections import INavigationSectionPosition
from Products.EEAContentTypes.interfaces import IFeedPortletInfo

def _get_contents(folder_brain, facetednav=None):
    """Get contents of folderish brain (cachable list/dict format)"""
    obj = folder_brain.getObject()
    if facetednav:
        query = facetednav.default_criteria
        brains = facetednav.query(batch=False, sort=True, **query)
    elif folder_brain.portal_type == 'Folder':
        brains = obj.getFolderContents()
    elif folder_brain.portal_type in ['Topic', 'RichTopic']:
        brains = obj.queryCatalog()
    return [{
        'title': brain.Title,
        'description': brain.Title,
        'url': brain.getURL(),
        'portal_type': brain.portal_type,
    } for brain in brains]

class DCViewLogic(BrowserView):
    """ View that shows the contents of all subfolders to the themecentre
    """

    def folder_contents(self, size_limit=10):
        """Get the folderish items in cachable list/dict format"""
        themecentre = getThemeCentre(self.context)
        size_limit = int(self.request.get('size_limit', size_limit))
        ret = {
            'folderish': [],
            'nonfolderish': [],
        }

        navSection = INavigationSectionPosition(self.context).section
        query = { 'navSection' : navSection}

        navtree_properties = getToolByName(self.context, 'portal_properties').navtree_properties
        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute
            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder

        for brain in themecentre.getFolderContents(contentFilter=query):
            if brain.getURL() == self.context.absolute_url():
                continue
            obj = brain.getObject()
            facetednav = queryMultiAdapter((obj, self.request), name=u'faceted_query')
            if (brain.portal_type in ['Folder', 'Topic', 'RichTopic']) or facetednav:
                contents = _get_contents(brain, facetednav)
                ret['folderish'].append({
                    'title': brain.Title,
                    'description': brain.Description,
                    'url': brain.getURL(),
                    'portal_type': brain.portal_type,
                    'contents': contents[:size_limit],
                    'has_more': len(contents) > size_limit,
                    'nitems': len(contents),
                })
            else:
                relatedObjects = obj.getRelatedItems()
                if relatedObjects:
                    for relatedObj in  relatedObjects:
                        if relatedObj.portal_type == 'RSSFeedRecipe':
                            feed = IFeedPortletInfo(IFeed(relatedObj))
                            ret['folderish'].append({
                                'title': brain.Title,
                                'description': brain.Description,
                                'url': brain.getURL(),
                                'portal_type': brain.portal_type,
                                'contents': [ {'title': item.title,
                                               'description': item.title,
                                               'url': item.url,
                                               'image' : item.image,
                                               'portal_type': 'FeedItem',
                                               } for item in feed.items[:size_limit] ],
                                'nitems': len(feed.items),
                                'has_more': True,
                                })

                else:
                    ret['nonfolderish'].append({
                        'title': brain.Title,
                        'description': brain.Description,
                        'url': brain.getURL(),
                        'portal_type': brain.portal_type,
                        })
        return ret
