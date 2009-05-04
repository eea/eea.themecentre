#
# Base TestCase for Audit
#

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure

dependencies = []

PRODUCTS = ('PloneRSSPortlet', 'ATVocabularyManager', 'LinguaPlone',
            'PloneHelpCenter', 'EEAContentTypes','valentine.linguaflow', 'PloneLanguageTool', 'EEAPloneAdmin',
            'FiveSite', 'ThemeCentre')



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
    for product in PRODUCTS:
        PloneTestCase.installProduct(product)


setup_themecentre()
PloneTestCase.setupPloneSite(products=PRODUCTS)

class ThemeCentreTestCase(PloneTestCase.FunctionalTestCase):
    """ Test case class used for functional themecentre tests. """
