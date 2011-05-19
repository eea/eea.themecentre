""" DC view logic
"""
from Products.CMFCore.utils import getToolByName
from eea.design.browser.subfolder_view_logic import SubFolderView
from eea.themecentre.themecentre import getThemeCentre
from Products.NavigationManager.interfaces import INavigationSectionPosition

class DCViewLogic(SubFolderView):
    """ View that shows the contents of all subfolders to the themecentre
    """

    def get_start_items(self):
        """ get start items
        """
        navSection = INavigationSectionPosition(self.context).section
        themecentre = getThemeCentre(self.context)
        query = {
            'navSection': navSection,
        }
        navtree_properties = \
           getToolByName(self.context, 'portal_properties').navtree_properties
        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute
            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder
        return themecentre.getFolderContents(contentFilter=query)
