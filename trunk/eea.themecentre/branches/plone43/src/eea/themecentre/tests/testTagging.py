""" Test tagging
"""
from unittest import TestSuite
from Testing.ZopeTestCase import FunctionalDocFileSuite
from zope.testing import doctest
from eea.themecentre.tests.base import EEAThemeCentreTestCase
from eea.themecentre.interfaces import IThemeTagging
from zope.app.component.hooks import setSite

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

class TestTagging(EEAThemeCentreTestCase):
    """ Test tagging
    """

    def afterSetUp(self):
        """ After setup
        """
        setSite(self.portal)
        self.setRoles(['Manager'])

        # make the air theme non deprecated
        air = self.portal.portal_vocabularies.themes.air
        self.portal.portal_workflow.doActionFor(air, 'publish')

def createObject(parent, portal_type, oid):
    """ Convenience method for creating and cataloging object
    """
    parent.invokeFactory(portal_type, id=oid)
    newobj = getattr(parent, oid, None)
    if newobj is not None:
        newobj.reindexObject()

class TestThemeCentre(EEAThemeCentreTestCase):
    """ Test Theme Centre
    """

    def afterSetUp(self):
        """ After setup
        """
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Folder', id='to_be_promoted')
        self.portal.invokeFactory('Folder', id='to_be_promoted2')
        self.portal.invokeFactory('Document', id='cut_and_paste')
        IThemeTagging(self.portal.cut_and_paste).tags = ['climate']
        self.portal.invokeFactory('Document', id='copy_and_paste')
        IThemeTagging(self.portal.copy_and_paste).tags = ['climate']
        self.createObject = createObject

        self.portal.invokeFactory('PressRelease', id='pr_link')
        self.portal.invokeFactory('Event', id='event_link')
        self.portal.invokeFactory('Document', id='doc_link')

def test_suite():
    """ Test suite
    """

    suite = TestSuite((
        FunctionalDocFileSuite('tagging.txt',
                     test_class=TestTagging,
                     package = 'eea.themecentre.tests',
                     optionflags=optionflags,
                     ),
        FunctionalDocFileSuite('themecentre.txt',
                     test_class=TestThemeCentre,
                     package = 'eea.themecentre.tests',
                     optionflags=optionflags,
                     ),
        FunctionalDocFileSuite('bugs.txt',
                     test_class=TestTagging,
                     package = 'eea.themecentre.tests',
                     optionflags=optionflags,
                     ),
        ))
    return suite
