from zope.interface import implements
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone import utils
from Products.CMFPlone.browser.interfaces import INavigationPortlet
from Products.CMFPlone.browser.portlets.navigation import NavigationPortlet as BaseNavigationPortlet
from eea.themecentre.themecentre import getThemeCentre

class NavigationPortlet(BaseNavigationPortlet):
    implements(INavigationPortlet)

    def title(self):
        return self.navigationRoot().Title()

    def createNavTree(self):
        context = utils.context(self)
        all = self.getNavTree()

        currentTheme = getThemeCentre(context)
        data = []
        if currentTheme is not None:
            data = [ node for node in all.get('children',[])
                                 if node['item'].getId == currentTheme.getId() ]
        
            path = '/'.join(context.getPhysicalPath())

            # we are not showing all levels so we want to set currentItem on higher
            # level if sub item is selected
            for node in data[0]['children']:
                if node['path'] in path:
                    node['currentItem'] = True
                    break
            
        properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(properties, 'navtree_properties')
        bottomLevel = navtree_properties.getProperty('bottomLevel', 0)
        
        return context.portlet_dropdown_navtree_macro(
            theme=data, children=all.get('children', []),
            level=1, show_children=True, isNaviTree=True, bottomLevel=4)

