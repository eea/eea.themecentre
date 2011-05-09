""" Test Doc Tests
"""
from unittest import TestSuite
from zope.interface import alsoProvides
from Testing.ZopeTestCase import FunctionalDocFileSuite
from zope.testing import doctest
from eea.themecentre.tests.ThemeCentreTestCase import ThemeCentreTestCase
from Products.CMFCore.utils import getToolByName
from eea.themecentre.interfaces import IThemeCentre, IThemeCentreSchema


class PortletTestCase(ThemeCentreTestCase):
    """ Portlet Test Case
    """

    def afterSetUp(self):
        """ After setup
        """
        portal = self.portal
        self.setRoles(['Manager'])

        portal.SITE.invokeFactory('Folder', id='themes')
        portal.SITE.themes.invokeFactory('Folder', id='energy')

        portal.SITE.reindexObject()
        portal.SITE.themes.reindexObject()
        portal.SITE.themes.energy.reindexObject()

        wf = getToolByName(portal, 'portal_workflow')
        wf.doActionFor(portal.SITE, 'publish')
        wf.doActionFor(portal.SITE.themes, 'publish')
        wf.doActionFor(portal.SITE.themes.energy, 'publish')

        context = portal.SITE.themes.energy
        alsoProvides(context, IThemeCentre)
        alsoProvides(context, IThemeCentreSchema)
        themecentre = IThemeCentreSchema(context)
        themecentre.tags = u'energy'


def test_suite():
    """ Test suite
    """

    return TestSuite((
        FunctionalDocFileSuite('promotion.txt',
                     package = 'eea.themecentre.browser.portlets',
                     test_class = PortletTestCase,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))
