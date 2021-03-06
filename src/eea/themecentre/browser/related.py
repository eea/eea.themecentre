""" Related
"""
from zope.interface import Interface
from zope.component import queryAdapter
from Products.CMFCore.utils import getToolByName

try:
    from Products.EEAContentTypes.interfaces import IRelations
except ImportError:
    class IRelations(Interface):
        """ IRelations """

from eea.themecentre.themecentre import getThemeCentre
from eea.themecentre.interfaces import IThemeTagging

# This is what is used in ZMI for navigation_sections_left and right
TOPICS_ID = 'topics'


class Topics(object):
    """ Provides related topic data for portlets.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def menu(self):
        """ Menu
        """
        plone_utils = getToolByName(self.context, 'plone_utils')
        propstool = getToolByName(self.context, 'portal_properties')
        siteprops = getattr(propstool, 'site_properties', None)
        if siteprops:
            view_actions = siteprops.getProperty(
                'typesUseViewActionInListings', [])
        else:
            view_actions = []

        themecentre = getThemeCentre(self.context)
        if themecentre is None:
            return None

        themecentre_url = themecentre.absolute_url()
        tags = IThemeTagging(themecentre).tags
        query = {'navSection': TOPICS_ID}
        memtool = getToolByName(self.context, 'portal_membership')
        if memtool is not None and memtool.isAnonymousUser():
            query['review_state'] = 'published'

        # get all objects that have the same theme as the current themecentre
        rel = queryAdapter(themecentre, IRelations)
        if rel:
            related_brains = rel.byTheme(getBrains=True, constraints=query)
            # ignore the objects that are stored in the current themecentre
            related_brains = [
                brain for brain in related_brains
                if not brain.getURL().startswith(themecentre_url)]
        else:
            related_brains = []

        menu = []
        for brain in related_brains:
            # check that the related object doesn't belong
            # to a deprecated theme
            themes = [theme for theme in brain.getThemes if theme not in tags]
            if themes:
                wf_state = plone_utils.normalizeString(brain.review_state)
                if brain.portal_type in view_actions:
                    url = brain.getURL() + '/view'
                else:
                    url = brain.getURL()

                item = {'title': brain.Title,
                        'url': url,
                        'portal_type': plone_utils.normalizeString(
                            brain.portal_type),
                        'wf_state': wf_state, }

                menu.append(item)

        menu.sort()
        return menu
