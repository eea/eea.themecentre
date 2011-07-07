""" Test theme centre
"""
from Products.ATContentTypes.content.newsitem import ATNewsItem
from eea.rdfrepository.rdfrepository import RDFRepository
from eea.themecentre.interfaces import IThemeTagging, IThemeTaggable
from eea.rdfrepository.interfaces import IRDFRepository
from zope.annotation.interfaces import IAnnotations
from zope.annotation.attribute import AttributeAnnotations
from zope.site.hooks import setSite
from zope.component import provideAdapter, provideUtility
from zope.interface import classImplements, alsoProvides
from unittest import TestSuite, makeSuite
from eea.themecentre.tests.base import EEAThemeCentreTestCase
from eea.themecentre.mergedtheme import ThemeTaggableMerged

class TestThemeCentre(EEAThemeCentreTestCase):
    """ Test Theme Centre
    """

    def afterSetUp(self):
        """ After setup
        """
        setSite(self.portal)

        provideAdapter(ThemeTaggableMerged)
        provideAdapter(AttributeAnnotations, provides=IAnnotations,
                adapts=[IThemeTaggable])
        provideUtility(RDFRepository())
        classImplements(ATNewsItem, IThemeTaggable)
        self.setRoles('Manager')

        # create and theme tag a news item
        self.portal.invokeFactory('News Item', id='news1')
        obj = self.portal.news1
        themes = IThemeTagging(obj)
        themes.tags = ['agriculture']
        self.portal.portal_catalog.reindexObject(self.portal.news1)

        alsoProvides(self.portal, IRDFRepository)
        self.portal.portal_catalog.reindexObject(self.portal)

    def testSearchTheme(self):
        """ There should be one item with the 'agriculture' themes tag
        """
        res = self.portal.portal_catalog.searchResults(
                                               getThemes=['agriculture'])
        self.assertEqual(len(res), 1)

    def testObjectProvides(self):
        """ We should find one news item that provides IThemeTaggable
        """
        catalog = self.portal.portal_catalog
        self.failUnless('object_provides' in catalog.indexes())

        res = catalog.searchResults(portal_type='News Item',
                object_provides='eea.themecentre.interfaces.IThemeTaggable')
        self.assertEqual(len(res), 1)

    def testMergedThemes(self):
        """ air_quality is merged with air
            create and theme tag a news item
        """
        self.portal.invokeFactory('News Item', id='news2')
        obj = self.portal.news2
        themes = IThemeTagging(obj)
        themes.tags = ['air']
        self.portal.portal_catalog.reindexObject(self.portal.news2)
        self.portal.invokeFactory('News Item', id='news3')
        obj = self.portal.news3
        themes = IThemeTagging(obj)
        themes.tags = ['air_quality']
        self.portal.portal_catalog.reindexObject(self.portal.news3)

        res = self.portal.portal_catalog.searchResults(
                getThemes=['air_quality'], portal_type='News Item')
        self.assertEqual(len(res), 1)
        # only air is mapped to air_quality not the other way around
        res = self.portal.portal_catalog.searchResults(
                                                     getThemes=['air'],
                                                     portal_type='News Item')
        self.assertEqual(len(res), 2)

def test_suite():
    """ Test suite
    """
    suite = TestSuite(makeSuite(TestThemeCentre))
    return suite
