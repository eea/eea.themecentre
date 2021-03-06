""" Test Doc Tests
"""
from unittest import TestSuite
from zope.interface import alsoProvides
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.CMFCore.utils import getToolByName

try:
    from eea.promotion import interfaces as HAS_PROMOTION
except ImportError:
    HAS_PROMOTION = False
from eea.themecentre.interfaces import IThemeCentre, IThemeCentreSchema
from eea.themecentre.tests.base import EEAThemeCentreTestCase


optionflags = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_ONLY_FIRST_FAILURE)


class PortletTestCase(EEAThemeCentreTestCase):
    """ Portlet Test Case
    """

    def afterSetUp(self):
        """ After setup
        """
        portal = self.portal
        self.setRoles(['Manager'])

        portal.invokeFactory('Folder', id='themes')
        portal.themes.invokeFactory('Folder', id='energy')

        portal.reindexObject()
        portal.themes.reindexObject()
        portal.themes.energy.reindexObject()

        wf = getToolByName(portal, 'portal_workflow')
        wf.doActionFor(portal.themes, 'publish')
        wf.doActionFor(portal.themes.energy, 'publish')

        context = portal.themes.energy
        alsoProvides(context, IThemeCentre)
        alsoProvides(context, IThemeCentreSchema)
        themecentre = IThemeCentreSchema(context)
        themecentre.tags = u'energy'


def test_suite():
    """ Test suite
    """
    suite = TestSuite()
    if HAS_PROMOTION:
        suite.addTest(
            FunctionalDocFileSuite('promotion.txt',
                                   package='eea.themecentre.browser.portlets',
                                   test_class=PortletTestCase,
                                   optionflags=optionflags,
                                   ),
        )
    return suite
