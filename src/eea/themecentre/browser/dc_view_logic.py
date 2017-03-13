""" DC view logic
"""
from Products.Five import BrowserView
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
from plone.portlets.interfaces import (
    IPortletRetriever,
    IPortletManager,
    IPortletRenderer
)

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
