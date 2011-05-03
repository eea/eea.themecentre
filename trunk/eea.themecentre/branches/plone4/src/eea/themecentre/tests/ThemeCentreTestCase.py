""" Base TestCase for Audit
"""
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure

PRODUCTS = ('EEAContentTypes',
            'valentine.linguaflow',
            'EEAPloneAdmin',
            'ThemeCentre')

PloneTestCase.installProduct('ATVocabularyManager')
PloneTestCase.installProduct('PloneHelpCenter')
PloneTestCase.installProduct('LinguaPlone')

@onsetup
def setup_themecentre():
    fiveconfigure.debug_mode = True
    import eea.themecentre
    zcml.load_config('configure.zcml', eea.themecentre)
    fiveconfigure.debug_mode = False

setup_themecentre()
PloneTestCase.setupPloneSite(extension_profiles=('eea.themecentre:default',))

class ThemeCentreTestCase(PloneTestCase.FunctionalTestCase):
    """ Test case class used for functional themecentre tests. """
