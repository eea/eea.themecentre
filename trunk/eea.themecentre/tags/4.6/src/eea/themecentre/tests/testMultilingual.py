""" Multilingual
"""
from zope.testing import doctest
from Products.ATContentTypes.content.newsitem import ATNewsItem
from eea.rdfrepository.rdfrepository import RDFRepository
from eea.themecentre.interfaces import (
    IThemeTaggable,
    IThemeCentreSchema
)
from eea.rdfrepository.interfaces import IRDFRepository
from zope.annotation.interfaces import IAnnotations
from zope.annotation.attribute import AttributeAnnotations
from zope.app.component.hooks import setSite
from zope.component import provideAdapter, provideUtility
from zope.interface import classImplements, alsoProvides
from Products.PloneTestCase.PloneTestCase import (
    default_user,
    default_password
)
from unittest import TestSuite
from Testing.ZopeTestCase import FunctionalDocFileSuite
from eea.themecentre.tests.base import EEAThemeCentreTestCase
from eea.themecentre.mergedtheme import ThemeTaggableMerged

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

class TestMultilingual(EEAThemeCentreTestCase):
    """ Test Multilingual
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

        wftool = self.portal.portal_workflow
        # create a swedish themecentre, an english feed folder and
        # a swedish feed
        self.portal.invokeFactory('Folder', id='svthemecentre')
        obj = self.portal.svthemecentre
        # turn the folder into a themecentre by calling the promote view
        # and setting a theme tag
        obj.unrestrictedTraverse('@@promote2ThemeCentre')()
        IThemeCentreSchema(obj).tags = 'climate'
        obj.setLanguage('sv')
        obj.intro.setLanguage('sv')
        wftool.doActionFor(obj, 'publish')
        obj.reindexObject()

        self.portal.invokeFactory('Folder', id='feedfolder')
        self.portal.feedfolder.setLanguage('en')
        alsoProvides(self.portal.feedfolder, IRDFRepository)
        self.portal.feedfolder.reindexObject()

        self.portal.portal_languages.addSupportedLanguage('sv')
        self.basic_auth = '%s:%s' % (default_user, default_password)

def test_suite():
    """ Suite
    """
    suite = TestSuite((
        FunctionalDocFileSuite('portlets.txt',
                     test_class=TestMultilingual,
                     package = 'eea.themecentre.tests',
                     optionflags=optionflags,
                     ),
        ))
    return suite
