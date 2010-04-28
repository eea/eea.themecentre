from Products.CMFPlone.PloneBatch import Batch
from Products.Five import BrowserView
from eea.themecentre.themecentre import getThemeCentre
from Products.NavigationManager.sections import INavigationSectionPosition


def _get_contents(folder_brain):
    """Get contents of folderish brain (cachable list/dict format)"""
    if folder_brain.portal_type == 'Folder':
        brains = folder_brain.getObject().getFolderContents()
    elif folder_brain.portal_type in ['Topic', 'RichTopic']:
        brains = folder_brain.getObject().queryCatalog()
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
        ret = []
        navSection = INavigationSectionPosition(self.context).section
        for brain in themecentre.getFolderContents(contentFilter={'navSection':navSection}):
            if brain.getURL() == self.context.absolute_url():
                continue
            item = {
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
                'portal_type': brain.portal_type,
                'folderish': False,
            }
            if brain.portal_type in ['Folder', 'Topic', 'RichTopic']:
                contents = _get_contents(brain)
                item['contents'] = contents[:size_limit]
                item['has_more'] = len(contents) > size_limit
                item['folderish'] = True
            ret.append(item)
        return ret
