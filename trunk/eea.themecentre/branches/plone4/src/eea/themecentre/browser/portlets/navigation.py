""" Navigation
"""
#TODO: fix me, plone4
#from zope.interface import implements
#from zope.component import getMultiAdapter
#from Products.CMFCore.utils import getToolByName
#from Products.CMFPlone.browser.interfaces import INavigationPortlet
#from eea.themecentre.themecentre import getThemeCentre
#import logging
#from Products.CMFPlone.browser.portlets.navigation import (
#    NavigationPortlet as BaseNavigationPortlet,
#)
##TODO: below is current location
##from plone.app.portlets.portlets.navigation import (
##    INavigationPortlet as BaseNavigationPortlet
##)

#logger = logging.getLogger("eea.themecentre")

#ITranslatable = None

#try:
    #from Products.LinguaPlone.interfaces import ITranslatable
#except ImportError:
    #logger.debug("ITranslatable not present")
## items that shouldn't be displayed in main meny
#blacklistedNavigationItems = []

#class NavigationPortlet(BaseNavigationPortlet):
    #implements(INavigationPortlet)

    #def display(self, section='default'):
        #default = BaseNavigationPortlet.display(self)
        #if default:
            #if section == 'default':
                #return True

            #context = self.context
            #currentTheme = getThemeCentre(context)
            #if currentTheme:
                #cat = getToolByName(context, 'portal_catalog')
                #query = {'path': '/'.join(currentTheme.getPhysicalPath()),
                         #'navSection': section}
                ## Filter on workflow states, if enabled
                #portal_properties = getToolByName(context, 'portal_properties')
                #navtree_properties = getattr(portal_properties,
                #                             'navtree_properties')
                #isAnon = getToolByName(context,
                #                       'portal_membership').isAnonymousUser()
                #prop_name = 'enable_wf_state_filtering'
                #enable_wf = navtree_properties.getProperty(prop_name, False)
                #if isAnon and enable_wf:
                    #query['review_state'] = \
                    #   navtree_properties.getProperty('wf_states_to_show', ())
                #result = cat.searchResults(query)
                #if len(result) > 0:
                    #return True
        #return False

    #def title(self):
        #return self.navigationRoot().Title()

    #def navigationRoot(self):
        #context = self.context
        #obj = getThemeCentre(context)
        #if obj is None:
            #obj = BaseNavigationPortlet.navigationRoot(self)
        #return obj

    #def createNavTree(self, section='default'):
        #if hasattr(self, '_all') and hasattr(self, '_data'):
            #return self.template(section)

        #context = self.context

        #self._all = all = self.getNavTree()

        #currentTheme = getThemeCentre(context)
        #data = []
        #if currentTheme is not None:
            ## find the node for current theme centre
            #for node in all.get('children', []):
                #if node['item'].getId == currentTheme.getId():
                    #data = node['children']
                    #break

        #newData = []
        #titles = []
        #for node in data:
            #nodeTitle = node['item']['Title']
            #if nodeTitle not in blacklistedNavigationItems:
                #if node['item'].getId == node['navSection'] and \
                                        #node['portal_type'] == 'Folder':
                    #parentSection = node['navSection']
                    ##depth = node['depth']
                    ## show children for a section which has
                    ## the same ID as a Folder
                    #children = node['children']
                    #if children == []:
                        #view = getMultiAdapter((node['item'].getObject(),
                                                 #self.request),
                                               #name='navtree_builder_view')
                        #tmp = view.navigationTree()
                        #for t in tmp['children']:
                            #if t['item'].getId == currentTheme.getId():
                                #break
                        #for t in t['children']:
                            #if t['path'] == node['path']:
                                #children = t['children']
                                #break

                    #for n in children:
                        #n['navSection'] = parentSection
                        #nodeTitle = n['item']['Title']
                        #newData.append(n)
                        #titles.append(nodeTitle)
                #else:
                    #newData.append(node)
                    #titles.append(nodeTitle)

        #data = newData

        ##data.extend(self._overview())

        ## order menu as configured in ZMI on themes
        #originalOrder = ['highlights',
                          #'reports',
                          #'indicators',
                          #'maps-and-graphs',
                          #'datasets',
                          #'events',
                          #'links']
        #if ITranslatable is not None and ITranslatable.providedBy(context):
            ## get order defined on canonical
            #originalOrder = getattr(context.getCanonical(),
                                     #'themes_menu_order',
                                     #originalOrder)
        ## try to get the order on a translation otherwise use one of above
        #order = getattr(context, 'themes_menu_order', originalOrder)

        #orderedData = [ None for n in range(0, len(order) + 1)]
        #unsortedData = []
        #for node in data:
            #n = 1
           ## default page always first
            #if  node.get('defaultPage', False):
                #orderedData[0] = node
            #else:
                #for urlPart in order:
                    #if urlPart in node['item'].getId:
                        #orderedData[n] = node
                        #break
                    #n += 1
                #else:
                    #unsortedData.append(node)
        #orderedData.extend(unsortedData)

        #navSections = {'default' : [] }
        #for node in orderedData:
            #if node is not None:
                #navSection = node['navSection']
                #sectionData = navSections.get(navSection, [])
                #sectionData.append(node)
                #navSections[navSection] = sectionData

        #self._data = navSections

        #return self.template(section)

    #def template(self, section='default'):
        #context = self.context
        #all = self._all
        #data = self._data.get(section, [])

        #return context.portlet_dropdown_navtree_macro(
                                 #theme=data,
                                 #children=all.get('children',[]),
                                 #level=1,
                                 #show_children=True,
                                 #isNaviTree=True,
                                 #bottomLevel=5)

    #def _overview(self):
        #context = self.context
        #tc = getThemeCentre(context)
        #if tc is not None:
            #url = tc.absolute_url() + '/overview'
            #currentItem = self.request.get('URL0','') == url
            #item = {'no_display': False,
                    #'getURL': url,
                    #'show_children': False,
                    #'Description': '',
                    #'Title': 'Overview',
                    #'absolute_url': url,
                    #'portal_type': 'RSSFeedRecipe',
                    #'Creator': '',
                    #'children': [],
                    #'currentParent': False,
                    #'creation_date': '2007-03-25 22:10:51',
                    #'item': None,
                    #'depth': 2,
                    #'path': '',
                    #'currentItem': currentItem,
                    #'review_state': '',
                    #'getRemoteUrl': None,
                    #'icon': 'www/folder_icon.gif'}

            #newNode = {'item'          : item,
                       #'getURL'        : url,
                       #'depth'         : '',
                       #'currentItem'   : currentItem,
                       #'currentParent' : False,
                       #'navSection'    : 'default',
                       #'children' : []}
            #return [newNode]
        #return []
