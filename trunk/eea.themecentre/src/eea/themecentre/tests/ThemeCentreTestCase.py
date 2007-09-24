#
# Base TestCase for Audit
#

import os, sys, code
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from zope.configuration.xmlconfig import XMLConfig
import Products.Five
import Products.FiveSite
import eea.themecentre

#XMLConfig('configure.zcml', Products.Five)()

dependencies = []
PloneTestCase.installProduct('Five')
PloneTestCase.installProduct('PloneRSSPortlet')
PloneTestCase.installProduct('ATVocabularyManager')
PloneTestCase.installProduct('EEAContentTypes')
PloneTestCase.installProduct('PloneHelpCenter')
PloneTestCase.installProduct('ThemeCentre')

XMLConfig('meta.zcml', Products.Five)()
XMLConfig('configure.zcml', Products.FiveSite)()
XMLConfig('configure.zcml', eea.themecentre)()

PRODUCTS = ('PloneRSSPortlet', 'ATVocabularyManager',
            'EEAContentTypes',
            'PloneHelpCenter',
            'FiveSite', 'ThemeCentre')

PloneTestCase.setupPloneSite(products=PRODUCTS)

class ThemeCentreTestCase(PloneTestCase.FunctionalTestCase):
    def interact(self, locals=None):
        savestdout = sys.stdout
        sys.stdout = sys.stderr
        sys.stderr.write("="*70)
        console = code.InteractiveConsole(locals)
        console.interact("""
ZopeTestCase Interactive Console
(c) BlueDynamics Alliance, Austria  - 2005

Note: You have the same locals available as in your test case.
""")
        sys.stdout.write('\nend of ZopeTestCase Interactive Console sessions\n')
        sys.stdout.write('='*70+'\n')
        sys.stdout = savestdout

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ThemeCentreTestCase))
    return suite

if __name__ == '__main__':
    framework()
