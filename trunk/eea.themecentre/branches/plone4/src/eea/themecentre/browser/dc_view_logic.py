""" DC view logic
"""
#from Products.CMFCore.utils import getToolByName
#from eea.design.browser.subfolder_view_logic import SubFolderView
#from eea.themecentre.themecentre import getThemeCentre
#from Products.NavigationManager.interfaces import INavigationSectionPosition

from Products.Five import BrowserView
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
from plone.portlets.interfaces import (
    IPortletRetriever,
    IPortletManager,
    IPortletRenderer
)

#class DCViewLogic(SubFolderView):
#    """ View that shows the contents of all subfolders to the themecentre
#    """
#
#    def get_start_items(self):
#        """ get start items
#        """
#        navSection = INavigationSectionPosition(self.context).section
#        themecentre = getThemeCentre(self.context)
#        query = {
#            'navSection': navSection,
#        }
#        navtree_properties = \\
#           getToolByName(self.context, 'portal_properties').navtree_properties
#        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
#        if sortAttribute is not None:
#            query['sort_on'] = sortAttribute
#            sortOrder = navtree_properties.getProperty('sortOrder', None)
#            if sortOrder is not None:
#                query['sort_order'] = sortOrder
#        return themecentre.getFolderContents(contentFilter=query)


def get_portlet_manager(column):
    """ Return one of default Plone portlet managers.
    """
    manager = getUtility(IPortletManager, name=column)
    return manager

def render_portlet(context, request, view, manager, interface):
    """ Render a portlet defined in external location.
    """

    retriever = getMultiAdapter((context, manager), IPortletRetriever)

    portlets = retriever.getPortlets()

    assignment = None

    for portlet in portlets:
        if interface.providedBy(portlet["assignment"]):
            assignment = portlet["assignment"]
            break

    if assignment is None:
        # Did not find a portlet
        return ""

    renderer = queryMultiAdapter((context, request, view, manager, assignment),
                                 IPortletRenderer)

    # Make sure we have working acquisition chain
    renderer = renderer.__of__(context)

    if renderer is None:
        raise RuntimeError("No portlet renderer found for \
                            portlet assignment:" + str(assignment))

    renderer.update()
    # Does not check visibility here... force render always
    html = renderer.render()
    return html


class DCViewLogic(BrowserView):
    """ Datacentre view logic """

    def render_nav_portlet(self):
        """ Render a portlet from another page in-line to this page
        Does not render other portlets in the same portlet manager.
        """
        context = self.context.aq_inner
        request = self.request
        view = self

        column = "plone.rightcolumn"
        from plone.app.portlets.portlets.navigation import INavigationPortlet
        manager = get_portlet_manager(column)
        html = render_portlet(context,
                              request,
                              view,
                              manager,
                              INavigationPortlet)
        return html
