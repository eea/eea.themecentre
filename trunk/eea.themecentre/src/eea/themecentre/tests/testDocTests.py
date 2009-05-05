import unittest
from zope.interface import alsoProvides
from Testing.ZopeTestCase import FunctionalDocFileSuite
from zope.testing import doctest
from ThemeCentreTestCase import ThemeCentreTestCase
from Products.CMFCore.utils import getToolByName
from eea.themecentre.interfaces import IThemeCentre, IThemeCentreSchema


class Test(ThemeCentreTestCase):

    def afterSetUp(self):
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

    return unittest.TestSuite((
        FunctionalDocFileSuite('promotion.txt',
                     package = 'eea.themecentre.browser.portlets',
                     test_class = Test,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
