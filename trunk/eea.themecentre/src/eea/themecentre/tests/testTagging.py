import unittest
from Testing.ZopeTestCase import FunctionalDocFileSuite
from zope.testing import doctest
from zope.component import provideAdapter
from zope.interface import classImplements
from eea.themecentre.themetaggable import ThemeTaggable, ThemeCentreTaggable
from eea.themecentre.tests.ThemeCentreTestCase import ThemeCentreTestCase
from eea.themecentre.interfaces import IThemeTagging
from zope.app.annotation.attribute import AttributeAnnotations
from zope.app.annotation.interfaces import IAttributeAnnotatable
from zope.app.component.hooks import setSite
from zope.app.folder.folder import Folder


class TestTagging(ThemeCentreTestCase):

    def afterSetUp(self):
        setSite(self.portal)
        self.setRoles(['Manager'])

        # make the air theme non deprecated
        air = self.portal.portal_vocabularies.themes.air
        self.portal.portal_workflow.doActionFor(air, 'publish') 

# convenience method for creating and cataloging object
def createObject(parent, portal_type, id):
    parent.invokeFactory(portal_type, id=id)
    newobj = getattr(parent, id, None)
    if newobj is not None:
        newobj.reindexObject()

class TestThemeCentre(ThemeCentreTestCase):

    def afterSetUp(self):
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

        # add one entry to the themes vocabulary
        vocab = self.portal.portal_vocabularies

def test_suite():

    suite = unittest.TestSuite((
        FunctionalDocFileSuite('tagging.txt',
                     test_class=TestTagging,
                     package = 'eea.themecentre.tests',
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        FunctionalDocFileSuite('themecentre.txt',
                     test_class=TestThemeCentre,
                     package = 'eea.themecentre.tests',
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
