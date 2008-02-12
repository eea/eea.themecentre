#
# Base TestCase for Audit
#

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure

dependencies = []

PRODUCTS = ('PloneRSSPortlet', 'ATVocabularyManager',
            'PloneHelpCenter',
            'FiveSite', 'ThemeCentre',
            'EEAContentTypes',)


@onsetup
def setup_themecentre():
    fiveconfigure.debug_mode = True
    import Products.Five
    import Products.FiveSite
    import eea.themecentre
    import Products.ThemeCentre
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', Products.FiveSite)
    zcml.load_config('configure.zcml', eea.themecentre)
    zcml.load_config('overrides.zcml', Products.ThemeCentre)
    fiveconfigure.debug_mode = False

    PloneTestCase.installProduct('Five')
    PloneTestCase.installProduct('PloneRSSPortlet')
    PloneTestCase.installProduct('ATVocabularyManager')
    PloneTestCase.installProduct('ThemeCentre')
    PloneTestCase.installProduct('PloneHelpCenter')
    PloneTestCase.installProduct('EEAContentTypes')

setup_themecentre()
PloneTestCase.setupPloneSite(products=PRODUCTS)

class ThemeCentreTestCase(PloneTestCase.FunctionalTestCase):
    """ Test case class used for functional themecentre tests. """
