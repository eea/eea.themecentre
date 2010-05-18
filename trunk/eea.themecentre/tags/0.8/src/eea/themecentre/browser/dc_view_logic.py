from zope.component import queryMultiAdapter
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from eea.rdfrepository.interfaces import IFeed
from eea.themecentre.themecentre import getThemeCentre
from Products.NavigationManager.sections import INavigationSectionPosition
from Products.EEAContentTypes.interfaces import IFeedPortletInfo

def _get_contents(folder_brain, size_limit, request, facetednav=None):
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
        'listing_url': getMultiAdapter((brain.getObject(), request), name=u'url').listing_url,
        'portal_type': brain.portal_type,
    } for brain in brains[:size_limit]], len(brains)

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
            listing_url = getMultiAdapter((obj, self.request), name=u'url').listing_url
            facetednav = queryMultiAdapter((obj, self.request), name=u'faceted_query')
            if (brain.portal_type in ['Folder', 'Topic', 'RichTopic']) or facetednav:
                contents, nitems = _get_contents(brain, size_limit, self.request, facetednav)
                ret['folderish'].append({
                    'title': brain.Title,
                    'description': brain.Description,
                    'url': brain.getURL(),
                    'listing_url': listing_url,
                    'portal_type': brain.portal_type,
                    'contents': contents,
                    'has_more': nitems > size_limit,
                    'nitems': nitems,
                })
            else:
                relatedObjects = obj.getRelatedItems()
                foundRSSFeedRecipe = False
                if relatedObjects:
                    for relatedObj in  relatedObjects:
                        if relatedObj.portal_type == 'RSSFeedRecipe':
                            feed = IFeedPortletInfo(IFeed(relatedObj))
                            ret['folderish'].append({
                                'title': brain.Title,
                                'description': brain.Description,
                                'url': brain.getURL(),
                                'listing_url': listing_url,
                                'portal_type': brain.portal_type,
                                'contents': [ {'title': item.title,
                                               'description': item.title,
                                               'url': item.url,
                                               'listing_url': item.url,
                                               'image' : item.image,
                                               'portal_type': 'FeedItem',
                                               } for item in feed.items[:size_limit] ],
                                'nitems': len(feed.items),
                                'has_more': len(feed.items) > size_limit,
                            })
                            foundRSSFeedRecipe = True
                if (not relatedObjects) or (not foundRSSFeedRecipe):
                    ret['nonfolderish'].append({
                        'title': brain.Title,
                        'description': brain.Description,
                        'url': brain.getURL(),
                        'listing_url': listing_url,
                        'portal_type': brain.portal_type,
                    })
        return ret
