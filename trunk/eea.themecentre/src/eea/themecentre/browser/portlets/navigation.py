from zope.interface import implements
from zope.component import getMultiAdapter

from Products.CMFPlone import utils
from Products.CMFPlone.browser.interfaces import INavigationPortlet
from Products.CMFPlone.browser.portlets.navigation import NavigationPortlet as BaseNavigationPortlet
from eea.themecentre.themecentre import getThemeCentre

# items that shouldn't be displayed in main meny
blacklistedNavigationItems = []

class NavigationPortlet(BaseNavigationPortlet):
    implements(INavigationPortlet)

    def __init__(self, context, request):
        super(NavigationPortlet, self).__init__(context, request)
        print "I N I T"

    def display(self, section='default'):
        print "D I S P L A Y"
        default = BaseNavigationPortlet.display(self)
        if default:
            if section == 'default':
                return True

            context = utils.context(self)
            currentTheme = getThemeCentre(context)
            if currentTheme:
                #cat = getToolByName(context, 'portal_catalog')
                #result = cat.searchResults( path = '/'.join(currentTheme.getPhysicalPath()), navSection=section)
                #if len(result) > 0: return True
                tree = self.createNavTree(section)
                if len(tree.strip()) > 0:
                    return True
        print "LEAVE D I S P L A Y"
        return False
    
    def title(self):
        return self.navigationRoot().Title()
    
    def navigationRoot(self):
        context = utils.context(self)
        obj = getThemeCentre(context)
        if obj is None:
            obj = BaseNavigationPortlet.navigationRoot(self)
        return obj

    def createNavTree(self, section='default'):
        print "ENTER C R E A T E"
        if hasattr(self, '_all') and hasattr(self, '_data'):
            return self.template(section)
        elif hasattr(self, '_html'):
            print "A L R E A D Y"
            return self._html
        print "C R E A T E N A V T R E E"
        context = utils.context(self)

        self._all = all = self.getNavTree()

        currentTheme = getThemeCentre(context)
        data = []
        if currentTheme is not None:
            # find the node for current theme centre
            for node in all.get('children',[]):
                if node['item'].getId == currentTheme.getId():
                    data = node['children']
                    break

        newData = []
        titles = []
        for node in data:
            nodeTitle = node['item']['Title']
            if nodeTitle not in blacklistedNavigationItems:
                if node['item'].getId == node['navSection'] and node['portal_type'] == 'Folder':
                    parentSection = node['navSection']
                    depth = node['depth']
                    # show children for a section which has the same ID as a Folder
                    children = node['children']
                    if children == []:
                        view = getMultiAdapter((node['item'].getObject(), self.request),
                                               name='navtree_builder_view')
                        print "T R E E"
                        tmp = view.navigationTree()
                        for t in tmp['children']:
                            if t['item'].getId == currentTheme.getId():
                                break
                        for t in t['children']:
                            if t['path'] == node['path']:
                                children = t['children']
                                break

                    for n in children:
                        n['navSection'] = parentSection
                        nodeTitle = n['item']['Title']
                        newData.append(n)
                        titles.append(nodeTitle)
                else:
                    newData.append(node)
                    titles.append(nodeTitle)

        data = newData

        #data.extend(self._overview())
        
        # order menu as configured in ZMI on themes
        order = getattr(context, 'themes_menu_order', ['highlights', 'reports', 'indicators', 'maps-and-graphs', 'datasets','events','links'])
        orderedData = [ None for n in range(0,len(order)+1)]
        unsortedData = []
        for node in data:
           n = 1
           # default page always first
           if  node.get('defaultPage', False):
               orderedData[0] = node
           else:
               for urlPart in order:
                   if urlPart in node['getURL']:
                       orderedData[n] = node
                       break
                   n += 1
               else:
                   unsortedData.append(node)
        orderedData.extend(unsortedData)

        navSections = {'default' : [] }
        for node in orderedData:
            if node is not None:
                navSection = node['navSection']
                sectionData = navSections.get(navSection, [])
                sectionData.append(node)                 
                navSections[navSection] = sectionData

        self._data = navSections
        self._html = self.template(section)
        print "L E A V E" 
        return self._html

    def template(self, section='default'):
        context = utils.context(self)
        all = self._all
        data = self._data.get(section, [])

        return context.portlet_dropdown_navtree_macro(
                                 theme=data, children=all.get('children',[]),
                                 level=1, show_children=True, isNaviTree=True, bottomLevel=5)

    def _overview(self):
        context = utils.context(self)
        tc = getThemeCentre(context)
        if tc is not None:
            url = tc.absolute_url() + '/overview'
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
                       'getURL'        : url,
                       'depth'         : '',
                       'currentItem'   : currentItem,
                       'currentParent' : False,
                       'navSection'    : 'default',
                       'children' : []}
            return [newNode]
        return []
