import unittest
from zope.testing import doctest
from zope.component import provideAdapter
from zope.interface import classImplements
from eea.themecentre.themetaggable import ThemeTaggable, ThemeCentreTaggable
from zope.app.annotation.attribute import AttributeAnnotations
from zope.app.annotation.interfaces import IAttributeAnnotatable
from zope.app.folder.folder import Folder

def setUp(test):
    provideAdapter(ThemeTaggable)
    provideAdapter(ThemeCentreTaggable)
    provideAdapter(AttributeAnnotations)
    classImplements(Folder, IAttributeAnnotatable)

def test_suite():

    return unittest.TestSuite((
        doctest.DocFileSuite('tagging.txt',
                     setUp=setUp, #tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        doctest.DocFileSuite('themecentre.txt',
                     setUp=setUp, #tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
