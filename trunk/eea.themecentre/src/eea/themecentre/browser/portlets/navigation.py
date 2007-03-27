from zope.interface import implements
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone import utils
from Products.CMFPlone.browser.interfaces import INavigationPortlet
from Products.CMFPlone.browser.portlets.navigation import NavigationPortlet as BaseNavigationPortlet
from eea.themecentre.themecentre import getThemeCentre

class NavigationPortlet(BaseNavigationPortlet):
    implements(INavigationPortlet)

    def title(self):
        return self.navigationRoot().Title()
    
    def navigationRoot(self):
        context = utils.context(self)
        obj = getThemeCentre(context)
        if obj is None:
            obj = BaseNavigationPortlet.navigationRoot(self)
        return obj
        
    def createNavTree(self):
        context = utils.context(self)
        all = self.getNavTree()

        currentTheme = getThemeCentre(context)
        data = []
        if currentTheme is not None:
            data = [ node for node in all.get('children',[])
                                 if node['item'].getId == currentTheme.getId() ]
            if len(data) > 0:
                data = data[0].get('children',[])
                
            path = '/'.join(context.getPhysicalPath())

            # we are not showing all levels so we want to set currentItem on higher
            # level if sub item is selected
            for node in data[0]['children']:
                if node['path'] in path:
                    node['currentItem'] = True
                    break

        products = self._products()
        titles = [ node['item']['Title'] for node in data ]
        for product in products:
            if product['item']['Title'] not in titles:
                data.append(product)

        data.append(self._overview())
        
        properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(properties, 'navtree_properties')
        bottomLevel = navtree_properties.getProperty('bottomLevel', 0)
        
        return context.portlet_dropdown_navtree_macro(
            theme=data, children=all.get('children', []),
            level=1, show_children=True, isNaviTree=True, bottomLevel=3)


    def _products(self):
        context = utils.context(self)
        view = getMultiAdapter((context, self.request),
                               name='themes-rdftitles')

        result = []
        for product in view.short_items():
            item = {'no_display': False,
                    'getURL': product['url'],
                    'show_children': False,
                    'Description': '',
                    'Title': product['title'],
                    'absolute_url': product['url'],
                    'portal_type': 'RSSFeedRecipe',
                    'Creator': '',
                    'children': [],
                    'currentParent': False,
                    'creation_date': '2007-03-25 22:10:51',
                    'item': None,
                    'depth': 2,
                    'path': '',
                    'currentItem': self.request.get('URL0','') == product['url'],
                    'review_state': '',
                    'getRemoteUrl': None,
                    'icon': 'www/folder_icon.gif'}

            newNode = {'item'          : item,
                       'depth'         : '',
                       'currentItem'   : self.request.get('URL0','') == product['url'],
                       'currentParent' : False,
                       'children' : []}
            
            result.append(newNode)
        return result
    
    def _overview(self):
        context = utils.context(self)
        tc = getThemeCentre(context)
        url = tc.absolute_url() + '/themecentre_overview'
        currentItem = self.request.get('URL0','') == url
        item = {'no_display': False,
                'getURL': url,
                'show_children': False,
                'Description': '',
                'Title': 'Overview',
                'absolute_url': url,
                'portal_type': 'RSSFeedRecipe',
                'Creator': '',
                'children': [],
                'currentParent': False,
                'creation_date': '2007-03-25 22:10:51',
                'item': None,
                'depth': 2,
                'path': '',
                'currentItem': currentItem,
                'review_state': '',
                'getRemoteUrl': None,
                'icon': 'www/folder_icon.gif'}

        newNode = {'item'          : item,
                   'depth'         : '',
                   'currentItem'   : currentItem,
                   'currentParent' : False,
                   'children' : []}

        return newNode
