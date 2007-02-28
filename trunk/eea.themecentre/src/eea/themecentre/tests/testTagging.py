import unittest
from Testing.ZopeTestCase import FunctionalDocFileSuite
from zope.testing import doctest
from zope.component import provideAdapter
from zope.interface import classImplements
from eea.themecentre.themetaggable import ThemeTaggable, ThemeCentreTaggable
from eea.themecentre.tests.ThemeCentreTestCase import ThemeCentreTestCase
from zope.app.annotation.attribute import AttributeAnnotations
from zope.app.annotation.interfaces import IAttributeAnnotatable
from zope.app.folder.folder import Folder

def setUp(test):
    provideAdapter(ThemeTaggable)
    provideAdapter(ThemeCentreTaggable)
    provideAdapter(AttributeAnnotations)
    classImplements(Folder, IAttributeAnnotatable)

def createObject(parent, portal_type, id):
    parent.invokeFactory(portal_type, id=id)
    newobj = getattr(parent, id, None)
    if newobj is not None:
        newobj.reindexObject()

class TestThemeCentre(ThemeCentreTestCase):
    def afterSetUp(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Folder', id='to_be_promoted')
        self.createObject = createObject

        # add one entry to the themes vocabulary
        vocab = self.portal.portal_vocabularies
        vocab.themes.invokeFactory('SimpleVocabularyTerm', 'air')
        vocab.themes['air'].setTitle('Air')


def test_suite():

    return unittest.TestSuite((
        doctest.DocFileSuite('tagging.txt',
                     setUp=setUp, #tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        FunctionalDocFileSuite('themecentre.txt',
                     test_class=TestThemeCentre,
                     package = 'eea.themecentre.tests',
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
